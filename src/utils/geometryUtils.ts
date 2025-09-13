export function distanceToLineSegmentSquared(x: number, y: number, x1: number, y1: number, x2: number, y2: number) {

    // This assumes an infinite line, not a line segment
    // For a line segment, we would need to check if the perpendicular from the point to the line
    // intersects the segment, and if not, return the distance to the nearest endpoint.
    const base = Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2);
    // const heightSquare = Math.abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1) / base;


    if (base === 0) return Math.pow(x - x2, 2) + Math.pow(y - y2, 2);
    let t = ((x - x1) * (x2 - x1) + (y - y1) * (y2 - y1)) / base;
    t = Math.max(0, Math.min(1, t));
    const heightSquare = Math.pow(x - (x1 + t * (x2 - x1)), 2) + Math.pow(y - (y1 + t * (y2 - y1)), 2);

    return heightSquare;
}

export function distanceToPolygon(x: number, y: number, polyPoints: Array<Array<number>>) {
    let minDist = Number.MAX_VALUE;
    for (let i = 0; i < polyPoints.length; i++) {
        // Point 2 is the next in line, wrapping around to the first point
        const x1 = polyPoints[i][0], y1 = polyPoints[i][1];
        const nextIdx = (i + 1) % polyPoints.length;
        const x2 = polyPoints[nextIdx][0], y2 = polyPoints[nextIdx][1];

        const distance = distanceToLineSegmentSquared(x, y, x1, y1, x2, y2);
        if (distance < minDist) {
            minDist = distance
        }
    }
    // By only taking the square root at the end, we avoid computing it multiple times
    return Math.sqrt(minDist)
}

export function pointInPolygon(x: number, y: number, polyPoints: Array<Array<number>>) {
    let inside = false;
    for (let i = 0, j = polyPoints.length - 1; i < polyPoints.length; j = i++) {
        const xi = polyPoints[i][0], yi = polyPoints[i][1];
        const xj = polyPoints[j][0], yj = polyPoints[j][1];
        if (((yi > y) != (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) {
            inside = !inside
        }
    }

    return inside;
}
