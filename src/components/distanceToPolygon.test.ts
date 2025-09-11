import { describe, it, expect } from 'vitest';
import { distanceToPolygon, distanceToLineSegmentSquared } from '../utils/geometryUtils';

describe('distance to line base intersection line segment', () => {
    it('horizontal line', () => {
        const x: number = 0, y: number = 2;
        const x1: number = -1, y1: number = 1, x2: number = 1, y2: number = 1;
        expect(distanceToLineSegmentSquared(x, y, x1, y1, x2, y2))
            .toBeCloseTo(1);
    });
    it('vertical line', () => {
        const x: number = 98, y: number = 20;
        const x1: number = 100, y1: number = 100, x2: number = 100, y2: number = -100;
        expect(distanceToLineSegmentSquared(x, y, x1, y1, x2, y2))
            .toBeCloseTo(4);
    });
    it('diagonal line', () => {
        const x: number = 95, y: number = 100;
        const x1: number = -100, y1: number = -100, x2: number = 100, y2: number = 100;
        expect(distanceToLineSegmentSquared(x, y, x1, y1, x2, y2))
            .toBeCloseTo(12.5);
    });
    it('on a diagonal line', () => {
        const x: number = 0, y: number = 0;
        const x1: number = -100, y1: number = -100, x2: number = 100, y2: number = 100;
        expect(distanceToLineSegmentSquared(x, y, x1, y1, x2, y2))
            .toBeCloseTo(0);
    });
    it('on a zero length line', () => {
        const x: number = 20, y: number = 0;
        const x1: number = 10, y1: number = 10, x2: number = 10, y2: number = 10;
        expect(distanceToLineSegmentSquared(x, y, x1, y1, x2, y2))
            .toBeCloseTo(2001);
    });
});

describe('distance to line base does NOT intersection line segment', () => {
    it('horizontal line', () => {
        const x: number = 2, y: number = 2;
        const x1: number = -1, y1: number = 1, x2: number = 1, y2: number = 1;
        expect(distanceToLineSegmentSquared(x, y, x1, y1, x2, y2))
        .toBeCloseTo(2);
    });
    it('vertical line', () => {
        const x: number = 2, y: number = 2;
        const x1: number = 1, y1: number = 1, x2: number = 1, y2: number = -1;
        expect(distanceToLineSegmentSquared(x, y, x1, y1, x2, y2))
        .toBeCloseTo(2);
    });
});

describe('point to square', () => {
    it('1 above', () => {
        const x: number = 0, y: number = 2;
        const polyPoints: Array<Array<number>> = [[1, 1], [1, -1], [-1, -1], [-1, 1]];
        expect(distanceToPolygon(x, y, polyPoints)).toBeCloseTo(1);
    });
    it('2 below', () => {
        const x: number = 0, y: number = -3;
        const polyPoints: Array<Array<number>> = [[1, 1], [1, -1], [-1, -1], [-1, 1]];
        expect(distanceToPolygon(x, y, polyPoints)).toBeCloseTo(2);
    });
    it('3 right', () => {
        const x: number = 4, y: number = 0;
        const polyPoints: Array<Array<number>> = [[1, 1], [1, -1], [-1, -1], [-1, 1]];
        expect(distanceToPolygon(x, y, polyPoints)).toBeCloseTo(3);
    });
    it('4 left', () => {
        const x: number = -5, y: number = 0;
        const polyPoints: Array<Array<number>> = [[1, 1], [1, -1], [-1, -1], [-1, 1]];
        expect(distanceToPolygon(x, y, polyPoints)).toBeCloseTo(4);
    });
});