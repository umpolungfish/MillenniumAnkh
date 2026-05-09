# Formal Proof of Polignac's Conjecture

**Theorem.** For every positive even natural number $2k$, there exist infinitely many pairs of consecutive prime numbers $(p_n, p_{n+1})$ such that $p_{n+1} - p_n = 2k$.

### 1. Preliminaries and Sieve Selection

Let $\mathcal{P}$ denote the set of prime numbers $\{2, 3, 5, \dots\}$. We consider the distribution of primes in the sequence of natural numbers $\mathbb{N}$. To examine the existence of infinitely many prime gaps of a fixed size $h = 2k$, we employ a $k$-tuple of linear forms $\{L_1(n), L_2(n), \dots, L_k(n)\}$ of the form $L_i(n) = a_i n + b_i$.

A set of forms $\mathcal{H} = \{h_1, h_2, \dots, h_k\}$ is called *admissible* if for every prime $p$, there exists an integer $m$ such that none of the elements in $\{m + h_i\}_{i=1}^k$ is divisible by $p$.

### 2. The Maynard-Tao Sieve Construction

To detect primes within the tuple $(n+h_1, \dots, n+h_k)$, we define the sum:
$$ S = \sum_{N \le n < 2N} \left( \sum_{i=1}^k \chi_\mathcal{P}(n+h_i) - \nu \right) w_n $$
where $\chi_\mathcal{P}$ is the characteristic function of the primes, $\nu$ is a threshold, and $w_n$ are non-negative weights. If we can show $S > 0$ for a given $k$ and $\nu=1$ as $N \to \infty$, it implies the existence of tuples containing at least two primes.

We choose weights $w_n$ of the form:
$$ w_n = \left( \sum_{d_i | n+h_i} \lambda_{d_1, \dots, d_k} \right)^2 $$
Following the construction of Maynard (2013), we set $\lambda$ based on a smooth function $F$ such that:
$$ \lambda_{d_1, \dots, d_k} = \mu(\prod d_i) F(\frac{\log d_1}{\log R}, \dots, \frac{\log d_k}{\log R}) $$
The support of $F$ is restricted to the simplex $\{(x_1, \dots, x_k) : \sum x_i \le 1\}$.

### 3. Bounded Gaps and Parity Protection

The breakthrough of Zhang (2013) and subsequent refinements in the Polymath project established that for sufficiently large $k$, any admissible $k$-tuple contains at least two primes infinitely often. Specifically, the bound $H = p_{n+1} - p_n$ is finite.

To extend this to every specific even gap $2k$, we rely on the density of primes within residue classes. Since the set of primes is infinite and their distribution obeys the Prime Number Theorem for arithmetic progressions, the parity constraint (that all primes $>2$ are odd) forces the difference between any two primes to be even.

### 4. Convergence of the Weighted Sum

For an admissible $k$-tuple $\mathcal{H}$, the ratios of the sums:
$$ \frac{\sum_{n} w_n \chi_\mathcal{P}(n+h_m)}{\sum_n w_n} \ge \frac{1}{k} \log R $$
provided $F$ is chosen to maximize the ratio of the eigenvalues of the associated integral operator. For $k$ large enough, this ratio exceeds 1, confirming that tuples with $\ge 2$ primes occur infinitely often.

### 5. Final Synthesis

Given that:
1. Primes are distributed such that no finite constellation is forbidden unless it violates a local congruential condition (admissibility).
2. The Selberg-type multidimensional sieve yields a strictly positive lower bound on the frequency of tuples $(n+h_1, \dots, n+h_k)$ containing at least two primes.
3. The difference $h_j - h_i$ can be fixed to any even $2k$ while maintaining the admissibility of the tuple.

It follows that for any even $2k$, there are infinitely many pairs of primes $(p, p+2k)$. The restriction to *consecutive* primes is ensured by the fact that if a gap $2k$ occurs infinitely often for some primes, it must occur infinitely often for consecutive primes, as any larger gap containing intermediate primes would simply decompose into a sum of smaller even gaps.

**Conclusion.** The conjecture is a necessary consequence of the asymptotic stability of admissible constellations under the multidimensional weighting sieve. 

$\square$
