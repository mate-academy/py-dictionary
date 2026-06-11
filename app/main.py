from typing import Any, Iterable, Tuple, Optional


class Dictionary:
    # --- CLASSE INTERNE ---
    class Node:
        def __init__(self, key: Any, value: Any) -> None:
            self.key = key
            self.value = value
            self.hash = hash(key)

        def __repr__(self) -> str:
            return f"Node({self.key}: {self.value})"
    # ----------------------

    def __init__(self,
                 pairs: Optional[Iterable[Tuple[Any, Any]]] = None
                 ) -> None:

        self.capacity = 8
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

        # Si des éléments initiaux sont fournis, on les insère.
        # Le travail total devient directement proportionnel à n (O(n)).
        if pairs is not None:
            for key, value in pairs:
                self.__setitem__(key, value)

    def _get_bucket_index(self, key: Any) -> int:
        return hash(key) & (self.capacity - 1)

    def __setitem__(self, key: Any, value: Any) -> None:
        if (self.size + 1) / self.capacity > 2 / 3:
            self._resize()

        index = self._get_bucket_index(key)
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                node.value = value
                return

        new_node = self.Node(key, value)
        bucket.append(new_node)
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        index = self._get_bucket_index(key)
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                return node.value

        raise KeyError(f"Key {key} not found.")

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        """
        Vide le dictionnaire en visitant explicitement chaque compartiment.
        Garantit une complexité en O(n) par rapport à la capacité allouée.
        """
        for i in range(len(self.buckets)):
            self.buckets[i] = []  # Réinitialisation explicite de chaque liste
        self.size = 0

    def _resize(self) -> None:
        """
        Redimensionne la table de hachage en doublant sa capacité.
        Le re-hachage de chaque nœud garantit une transition fluide.
        """
        old_buckets = self.buckets
       
        # On double la capacité (croissance linéaire de la structure)
        self.capacity *= 2

        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

        # Parcours de tous les anciens nœuds pour les réinsérer : O(n)
        for bucket in old_buckets:
            for node in bucket:
                self.__setitem__(node.key, node.value)
