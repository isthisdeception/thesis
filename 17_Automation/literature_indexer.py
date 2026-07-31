#!/usr/bin/env python3
"""
Literature Indexer & Relationship Graph Generator (STEP-013)

Parses 02_Literature/metadata/papers.csv and all summary files in 02_Literature/summaries/
to deterministically generate 5 index files and 1 relationship graph CSV.

Outputs:
  - 02_Literature/indexes/keyword_index.csv
  - 02_Literature/indexes/author_index.csv
  - 02_Literature/indexes/venue_index.csv
  - 02_Literature/indexes/dataset_index.csv
  - 02_Literature/indexes/model_index.csv
  - 02_Literature/indexes/citation_network.csv
"""

import os
import re
import csv
from collections import defaultdict
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
LITERATURE_DIR = BASE_DIR / "02_Literature"
PAPERS_CSV = LITERATURE_DIR / "metadata" / "papers.csv"
SUMMARIES_DIR = LITERATURE_DIR / "summaries"
INDEXES_DIR = LITERATURE_DIR / "indexes"

def clean_str(val):
    """Strip whitespace and quotes."""
    if not val:
        return ""
    return val.strip().strip('"').strip("'")

def parse_list(val_str, delimiters=[',', ';']):
    """Split a string by delimiters and return a list of clean tokens."""
    if not val_str or val_str.lower() in ['unknown', 'none', 'n/a', 'not reported']:
        return []
    pattern = '|'.join(map(re.escape, delimiters))
    tokens = re.split(pattern, val_str)
    res = []
    for t in tokens:
        item = clean_str(t)
        if item and item.lower() not in ['unknown', 'none', 'n/a', 'not reported']:
            res.append(item)
    return res

def parse_authors(author_str):
    """Parse author names handling 'and', commas, and full names."""
    if not author_str or author_str.lower() in ['unknown', 'none']:
        return []
    # Replace ' and ' with comma
    s = re.sub(r'\s+and\s+', ', ', author_str, flags=re.IGNORECASE)
    parts = s.split(',')
    authors = []
    for p in parts:
        name = clean_str(p)
        if name and len(name) > 1:
            authors.append(name)
    return authors

def main():
    INDEXES_DIR.mkdir(parents=True, exist_ok=True)

    # Data structures for indexing
    keywords_map = defaultdict(set)
    authors_map = defaultdict(set)
    venues_map = defaultdict(set)
    datasets_map = defaultdict(set)
    models_map = defaultdict(set)
    
    # Store metadata per paper for relationship extraction
    paper_data = {}

    # 1. Read papers.csv
    if not PAPERS_CSV.exists():
        raise FileNotFoundError(f"Missing {PAPERS_CSV}")

    with open(PAPERS_CSV, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = clean_str(row.get('Paper ID'))
            if not pid:
                continue

            title = clean_str(row.get('Title'))
            authors_raw = clean_str(row.get('Authors'))
            venue = clean_str(row.get('Venue'))
            keywords_raw = clean_str(row.get('Keywords'))
            dataset_raw = clean_str(row.get('Dataset'))
            architecture_raw = clean_str(row.get('Architecture'))
            task = clean_str(row.get('Task'))

            authors = parse_authors(authors_raw)
            keywords = parse_list(keywords_raw)
            datasets = parse_list(dataset_raw)
            models = parse_list(architecture_raw)

            paper_data[pid] = {
                'title': title,
                'authors': authors,
                'venue': venue,
                'keywords': keywords,
                'datasets': datasets,
                'models': models,
                'task': task,
                'summary_connections': []
            }

            # Map to indexes
            for a in authors:
                authors_map[a].add(pid)
            
            if venue and venue.lower() not in ['unknown', 'none']:
                venues_map[venue].add(pid)
            
            for k in keywords:
                keywords_map[k].add(pid)

            for d in datasets:
                datasets_map[d].add(pid)

            for m in models:
                models_map[m].add(pid)

    # 2. Read summaries for additional features & connections
    if SUMMARIES_DIR.exists():
        for summary_file in sorted(SUMMARIES_DIR.glob("P*_summary.md")):
            pid = summary_file.stem.replace("_summary", "")
            if pid not in paper_data:
                continue

            content = summary_file.read_text(encoding='utf-8')
            
            # Extract Connections section
            conn_match = re.search(r'## Connections\s*\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
            if conn_match:
                conn_text = conn_match.group(1)
                # Find all Pxxxx references
                referenced_pids = re.findall(r'P\d{4}', conn_text)
                for ref_pid in referenced_pids:
                    if ref_pid != pid and ref_pid in paper_data:
                        paper_data[pid]['summary_connections'].append(ref_pid)

    # Helper function to write standard index CSV
    def write_index(filename, header_key_name, data_map):
        filepath = INDEXES_DIR / filename
        sorted_keys = sorted(data_map.keys(), key=lambda x: x.lower())
        with open(filepath, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([header_key_name, "Paper Count", "Paper IDs"])
            for key in sorted_keys:
                pids = sorted(list(data_map[key]))
                writer.writerow([key, len(pids), "; ".join(pids)])

    # Write 5 Indexes
    write_index("keyword_index.csv", "Keyword", keywords_map)
    write_index("author_index.csv", "Author", authors_map)
    write_index("venue_index.csv", "Venue", venues_map)
    write_index("dataset_index.csv", "Dataset", datasets_map)
    write_index("model_index.csv", "Model", models_map)

    # 3. Build Citation Network / Relationship Graph
    edges = []
    seen_edges = set()

    # Rule A: Explicit summary cross-references
    for pid, data in paper_data.items():
        for target_pid in data['summary_connections']:
            edge_key = (pid, target_pid, "cross_reference")
            if edge_key not in seen_edges:
                seen_edges.add(edge_key)
                edges.append({
                    'source': pid,
                    'target': target_pid,
                    'type': "cross_reference",
                    'field': "Summary Connections",
                    'evidence': f"Explicit connection cited in {pid}_summary.md"
                })

    # Rule B: Same research group (co-authoring multiple papers in our registry)
    group_author_papers = defaultdict(list)
    for pid, data in paper_data.items():
        for author in data['authors']:
            group_author_papers[author].append(pid)

    for author, pids in group_author_papers.items():
        if len(pids) > 1:
            sorted_pids = sorted(pids)
            for i in range(len(sorted_pids)):
                for j in range(i + 1, len(sorted_pids)):
                    p1, p2 = sorted_pids[i], sorted_pids[j]
                    edge_key = (p1, p2, "same_research_group")
                    if edge_key not in seen_edges:
                        seen_edges.add(edge_key)
                        edges.append({
                            'source': p1,
                            'target': p2,
                            'type': "same_research_group",
                            'field': "Authors",
                            'evidence': f"Co-authored by {author}"
                        })

    # Rule C: Shared benchmark dataset
    for dataset, pids in datasets_map.items():
        if len(pids) > 1 and dataset.lower() not in ['unknown', 'none', 'custom']:
            sorted_pids = sorted(list(pids))
            for i in range(len(sorted_pids)):
                for j in range(i + 1, len(sorted_pids)):
                    p1, p2 = sorted_pids[i], sorted_pids[j]
                    edge_key = (p1, p2, "same_dataset")
                    if edge_key not in seen_edges:
                        seen_edges.add(edge_key)
                        edges.append({
                            'source': p1,
                            'target': p2,
                            'type': "same_dataset",
                            'field': "Dataset",
                            'evidence': f"Evaluated on shared benchmark dataset: {dataset}"
                        })

    # Sort edges deterministically
    edges.sort(key=lambda e: (e['source'], e['target'], e['type'], e['evidence']))

    # Write citation_network.csv
    citation_network_path = INDEXES_DIR / "citation_network.csv"
    with open(citation_network_path, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Source Paper ID", "Target Paper ID", "Relationship Type", "Source Field", "Evidence"])
        for edge in edges:
            writer.writerow([edge['source'], edge['target'], edge['type'], edge['field'], edge['evidence']])

    print(f"STEP-013 Indexing Complete.")
    print(f"  - Keywords: {len(keywords_map)}")
    print(f"  - Authors: {len(authors_map)}")
    print(f"  - Venues: {len(venues_map)}")
    print(f"  - Datasets: {len(datasets_map)}")
    print(f"  - Models: {len(models_map)}")
    print(f"  - Relationship Edges: {len(edges)}")

if __name__ == "__main__":
    main()
