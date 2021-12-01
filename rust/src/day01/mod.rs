#[aoc_generator(day1)]
pub fn parse_input(input: &str) -> Vec<u32> {
    input.lines().map(|n| n.parse().unwrap()).collect()
}

#[aoc(day1, part1)]
pub fn solve_part1(input: &[u32]) -> u32 {
    let first = input[0];
    let (_, increased) = input
        .iter()
        .skip(1)
        .fold((first, 0), |(p, i), &n| (n, if n > p { i + 1 } else { i }));
    increased
}

#[aoc(day1, part2)]
pub fn solve_part2(input: &[u32]) -> u32 {
    let mut prev: u32 = input[..3].iter().sum();
    let mut increased = 0;
    for i in 1..(input.len() - 2) {
        let crnt = input[i..(i + 3)].iter().sum();
        if crnt > prev {
            increased += 1;
        }
        prev = crnt;
    }
    increased
}
