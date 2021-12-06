#[aoc_generator(day6)]
pub fn parse_input(input: &str) -> [u64; 9] {
    let mut counts = [0; 9];
    for s in input.split_terminator(",") {
        let n: usize = s.parse().unwrap();
        counts[n] += 1;
    }
    counts
}

#[aoc(day6, part1)]
pub fn solve_part1(input: &[u64; 9]) -> u64 {
    simulate_growth(*input, 80)
}

#[aoc(day6, part2)]
pub fn solve_part2(input: &[u64; 9]) -> u64 {
    simulate_growth(*input, 256)
}

fn simulate_growth(mut counts: [u64; 9], cycles: usize) -> u64 {
    let mut zero_idx = 0;
    for _ in 0..cycles {
        counts[(zero_idx + 7) % 9] += counts[zero_idx];
        zero_idx = (zero_idx + 1) % 9;
    }
    counts.iter().sum()
}
