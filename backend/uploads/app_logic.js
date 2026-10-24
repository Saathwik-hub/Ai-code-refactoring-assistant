// Developer Assistant JS Demo
function calculateStats(items) {
    if (!Array.isArray(items)) {
        throw new Error("Invalid input: expected array");
    }
    const total = items.reduce((acc, curr) => acc + curr, 0);
    const average = total / items.length;
    return { total, average, count: items.length };
}

console.log(calculateStats([10, 20, 30, 40, 50]));
