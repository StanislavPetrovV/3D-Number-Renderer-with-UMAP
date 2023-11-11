from numba import njit
import numpy as np
import scipy
import umap


@njit(cache=True)
#
def is_prime(num):
    if num == 2:
        return True
    if num < 2 or not num % 2:
        return False
    for i in range(3, int(num ** 0.5) + 1, 2):
        if not num % i:
            return False
    return True


@njit(cache=True)
#
def get_prime_hash_map(numbers):
    prime_hashmap_ = {2: 0}
    #
    idx = 1
    for n in range(3, numbers + 1, 2):
        if is_prime(n):
            prime_hashmap_[n] = idx
            idx += 1
    #
    return prime_hashmap_


@njit(cache=True)
#
def get_composite_number_factors(num, prime_hashmap_):
    factors_ = set()
    #
    for prime in prime_hashmap_:
        #
        while not num % prime:
            num //= prime
            factors_.add(prime)
        #
        if num == 1:
            break
        #
        if num in prime_hashmap_:
            factors_.add(num)
            break
    return factors_


def fill_array(numbers, prime_hashmap_, factor_array_):
    for n in range(2, numbers):
        #
        if n in prime_hashmap_:
            idx = prime_hashmap_[n]
            factor_array_[n, idx] = 1
            continue
        #
        factors = get_composite_number_factors(num=n, prime_hashmap_=prime_hashmap_)
        for factor in factors:
            idx = prime_hashmap_[factor]
            factor_array_[n, idx] = 1
    #
    return factor_array_


if __name__ == '__main__':
    # amount of numbers
    N = 10_000

    # get all primes up to N
    prime_hashmap = get_prime_hash_map(N)

    # result array
    factor_array = scipy.sparse.lil_matrix((N, len(prime_hashmap)), dtype=np.int8)

    # factorization
    factor_array = fill_array(
        numbers=N, prime_hashmap_=prime_hashmap, factor_array_=factor_array
    )

    # umap settings
    n_neighbors = 15
    min_dist = 0.2
    n_components = 3
    n_epochs = 500
    metric = 'cosine'

    # training
    map_data = umap.UMAP(
        metric=metric,
        n_epochs=n_epochs,
        n_components=n_components,
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        low_memory=True
    ).fit_transform(factor_array)

    # save result
    np.save(f'data/map_data_3d_{N}_{n_neighbors}_{str(min_dist).replace(".", "")}', map_data)
