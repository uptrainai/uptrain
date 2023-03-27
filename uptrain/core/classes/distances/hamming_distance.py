import numpy as np

from typing import List, Union

from uptrain.core.classes.distances import AbstractDistance


class HammingDistance(AbstractDistance):
    """Class that computes Hamming distance between base and reference vectors."""

    def check_valid_vector(self, vector) -> None:
        if not np.all(np.isin(vector, [0, 1])):
            raise Exception("Vector should contain only 0 and 1")

    def compute_distance(
        self, base: Union[List, np.ndarray], reference: Union[List, np.ndarray]
    ) -> int:
        """Compute the Hamming distance between base and reference vectors.

        Parameters
        ----------
        base
            It is the base vector for Hamming distance computation.
        reference
            It is the reference vector for Hamming distance computation.

        Returns
        -------
        int
            The Hamming distance between base and reference.
        """

        base = np.array(base)
        reference = np.array(reference)

        self.check_valid_vector(base)
        self.check_valid_vector(reference)

        self.check_compatibility(base, reference)

        return np.sum(np.sum(base != reference, axis=tuple(range(1, len(base.shape)))))
