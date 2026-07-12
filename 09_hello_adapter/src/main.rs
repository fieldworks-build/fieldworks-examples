//! Hello adapter: the protocol layer in isolation. Spins up an embedded
//! MQTT broker, seeds one retained value, spawns the real `mqtt-mcp`
//! binary as an MCP server over stdio, and calls `connect` + `read_tag`
//! to get a VQT envelope back. No topology, no agents, no aggregator.

use std::collections::HashMap;
use std::env;
use std::process::Stdio;
use std::time::Duration;

use rmcp::model::CallToolRequestParams;
use rmcp::transport::{ConfigureCommandExt, TokioChildProcess};
use rmcp::ServiceExt;
use rumqttc::{AsyncClient, MqttOptions, QoS};
use rumqttd::{Broker, Config, ConnectionSettings, RouterConfig, ServerSettings};
use serde_json::json;
use tokio::process::Command;

const BROKER_PORT: u16 = 18830;
const TOPIC: &str = "factory/pump01/flow_rate";

/// Build a minimal single-listener rumqttd config and run it to completion
/// on a dedicated OS thread — `Broker::start()` blocks the calling thread
/// by design, so it can never share a thread with the async work below.
fn start_embedded_broker() {
    let router = RouterConfig {
        max_connections: 100,
        max_outgoing_packet_count: 200,
        max_segment_size: 104_857_600,
        max_segment_count: 10,
        ..Default::default()
    };

    let mut v4 = HashMap::new();
    v4.insert(
        "v4-1".to_string(),
        ServerSettings {
            name: "v4-1".to_string(),
            listen: format!("127.0.0.1:{BROKER_PORT}").parse().unwrap(),
            tls: None,
            next_connection_delay_ms: 1,
            connections: ConnectionSettings {
                connection_timeout_ms: 60_000,
                max_payload_size: 20_480,
                max_inflight_count: 100,
                auth: None,
                external_auth: None,
                dynamic_filters: true,
            },
        },
    );

    let config = Config {
        id: 0,
        router,
        v4: Some(v4),
        ..Default::default()
    };

    std::thread::spawn(move || {
        Broker::new(config)
            .start()
            .expect("embedded broker crashed");
    });
}

async fn wait_for_broker() {
    for _ in 0..50 {
        if tokio::net::TcpStream::connect(("127.0.0.1", BROKER_PORT))
            .await
            .is_ok()
        {
            return;
        }
        tokio::time::sleep(Duration::from_millis(100)).await;
    }
    panic!("embedded broker never came up on 127.0.0.1:{BROKER_PORT}");
}

/// Publish one *retained* value before mqtt-mcp ever subscribes. read_tag
/// subscribes and waits for a message with a 10s timeout — retained
/// messages are what let that work without racing a live publish.
async fn seed_retained_value() -> anyhow::Result<()> {
    let mut opts = MqttOptions::new("hello-adapter-seed", "127.0.0.1", BROKER_PORT);
    opts.set_keep_alive(Duration::from_secs(5));
    let (client, mut eventloop) = AsyncClient::new(opts, 10);

    // rumqttc only does I/O when its event loop is polled.
    tokio::spawn(async move { while eventloop.poll().await.is_ok() {} });

    let payload = json!({ "value": 312.7, "units": "gpm" }).to_string();
    client
        .publish(TOPIC, QoS::AtLeastOnce, /* retain */ true, payload)
        .await?;

    // Give the background poll task time to actually flush the publish.
    tokio::time::sleep(Duration::from_millis(300)).await;
    Ok(())
}

fn tool_args(value: serde_json::Value) -> serde_json::Map<String, serde_json::Value> {
    value.as_object().expect("literal object").clone()
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    println!("starting an embedded MQTT broker on 127.0.0.1:{BROKER_PORT}...");
    start_embedded_broker();
    wait_for_broker().await;

    println!("seeding a retained value on '{TOPIC}'...");
    seed_retained_value().await?;

    let mqtt_mcp_bin = env::var("MQTT_MCP_BIN").unwrap_or_else(|_| "mqtt-mcp".to_string());
    println!("spawning '{mqtt_mcp_bin}' as an MCP server over stdio...");

    let command = Command::new(&mqtt_mcp_bin).configure(|cmd| {
        cmd.stderr(Stdio::null());
    });
    let client = ().serve(TokioChildProcess::new(command)?).await?;

    println!("calling connect...");
    client
        .call_tool(
            CallToolRequestParams::new("connect").with_arguments(tool_args(
                json!({ "host": "127.0.0.1", "port": BROKER_PORT }),
            )),
        )
        .await?;

    println!("calling read_tag('{TOPIC}')...");
    let result = client
        .call_tool(
            CallToolRequestParams::new("read_tag")
                .with_arguments(tool_args(json!({ "tag_id": TOPIC }))),
        )
        .await?;

    println!("\nVQT envelope:");
    println!(
        "{}",
        serde_json::to_string_pretty(&result.structured_content)?
    );

    client.cancel().await?;
    Ok(())
}
