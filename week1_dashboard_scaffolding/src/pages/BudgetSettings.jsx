function BudgetSettings() {
  return (
    <div style={{ padding: "2rem" }}>
      <h1>Set Budget Constraints</h1>
      <p>Define the total marketing budget to optimize discount allocation.</p>
      <label>
        Total Budget ($):
        <input type="number" placeholder="5000" />
      </label>
    </div>
  );
}

export default BudgetSettings;
