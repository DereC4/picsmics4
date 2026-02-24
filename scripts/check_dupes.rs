use std::{collections::HashMap, fs};
use serde_json::Value;

fn main() {
  let comments: Vec<Value> =
    serde_json::from_str(&fs::read_to_string("docs/comments.json").unwrap()).unwrap();
  let mut seen: HashMap<(String, String, i64), usize> = HashMap::new();
  let mut dupes = 0;
  for (i, c) in comments.iter().enumerate() {
    let k = (
      c["id"].as_str().unwrap_or("").into(),
      c["text"].as_str().unwrap_or("").into(),
      c["timestamp"].as_i64().unwrap_or(0),
    );
    
    if let Some(&first) = seen.get(&k) {
      dupes += 1;
      println!(
        "  Index {} dupes index {} | id={} | ts={} | text={:.80}",
        i, first, k.0, k.2, k.1
      );
    } else {
      seen.insert(k, i);
    }
  }
  println!(
    "{}",
    if dupes > 0 {
      format!("Found {} duplicate(s)", dupes)
    } else {
      format!("No duplicates among {} comments.", comments.len())
    }
  );
}