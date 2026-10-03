function UploadData() {
  return (
    <div style={{ padding: "2rem" }}>
      <h1>Upload Historical Campaign Data</h1>
      <p>Upload a CSV of past campaign results to train the causal model.</p>
      <input type="file" accept=".csv" />
    </div>
  );
}

export default UploadData;
