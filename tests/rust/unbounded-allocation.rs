use std::collections::HashMap;

pub struct Vertex {
    pub x: i64,
    pub y: i64,
}

// The shape of parse_polyline before 1.2.1: only a lower bound was checked.
pub fn parse_polyline(props: &HashMap<String, String>) -> Result<Vec<Vertex>, String> {
    let count: usize = props
        .get("LocationCount")
        .ok_or("missing")?
        .parse::<usize>()
        .map_err(|e| e.to_string())?;
    if count < 2 {
        return Err("too few points".into());
    }
    // ruleid: rust-allocation-sized-by-parsed-count
    let mut points = Vec::with_capacity(count);
    for i in 1..=count {
        let x = props.get(&format!("X{i}")).and_then(|v| v.parse().ok()).unwrap_or(0);
        let y = props.get(&format!("Y{i}")).and_then(|v| v.parse().ok()).unwrap_or(0);
        points.push(Vertex { x, y });
    }
    Ok(points)
}

// Fixed shape: a record can describe at most one vertex per key, plus a few.
pub fn parse_polyline_fixed(props: &HashMap<String, String>) -> Result<Vec<Vertex>, String> {
    let count: usize = props
        .get("LocationCount")
        .ok_or("missing")?
        .parse::<usize>()
        .map_err(|e| e.to_string())?;
    if count > props.len() + 2 {
        return Err("LocationCount larger than the record".into());
    }
    // ok: rust-allocation-sized-by-parsed-count
    let points = Vec::with_capacity(count);
    Ok(points)
}

pub fn header_components(bytes: &[u8]) -> Vec<String> {
    let n = u32::from_le_bytes([bytes[0], bytes[1], bytes[2], bytes[3]]) as usize;
    // ruleid: rust-allocation-sized-by-parsed-count
    let mut names = Vec::<String>::with_capacity(n);
    names.push(String::new());
    // ok: rust-allocation-sized-by-parsed-count
    let capped = Vec::<u8>::with_capacity(n.min(bytes.len()));
    drop(capped);
    names
}

// The LibRef{idx} shape: the index suffix of a key drives a growth loop.
pub fn lib_refs(props: &HashMap<String, String>) -> Vec<String> {
    let mut refs: Vec<String> = Vec::new();
    for (key, value) in props {
        if let Some(suffix) = key.strip_prefix("LibRef") {
            if let Ok(idx) = suffix.parse::<usize>() {
                // ruleid: rust-grow-loop-driven-by-parsed-index
                while refs.len() <= idx {
                    refs.push(String::new());
                }
                refs[idx] = value.clone();
            }
        }
    }
    refs
}

pub fn lib_refs_fixed(props: &HashMap<String, String>, field_count: usize) -> Vec<String> {
    let mut refs: Vec<String> = Vec::new();
    for (key, value) in props {
        if let Some(suffix) = key.strip_prefix("LibRef") {
            if let Ok(idx) = suffix.parse::<usize>() {
                if idx >= field_count {
                    continue;
                }
                // ok: rust-grow-loop-driven-by-parsed-index
                while refs.len() <= idx {
                    refs.push(String::new());
                }
                refs[idx] = value.clone();
            }
        }
    }
    refs
}
