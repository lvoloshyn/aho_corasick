# Based on https://github.com/abusix/ahocorapy
from typing import Collection, Optional, Any, Generator, Tuple, Dict, List


class State:
    def __init__(self,
                 identifier: int,
                 token: Optional[Any] = None,
                 parent: Optional["State"] = None,
                 success: bool = False):
        self.token = token
        self.identifier = identifier
        self.transitions: Dict[Any, "State"] = {}
        self.parent = parent
        self.success = success

        self.matched_tokens = Collection[Any]
        self.matched_tokens_index: Optional[int] = None
        self.longest_strict_suffix: Optional["State"] = None


class TokenTree:
    def __init__(self):
        self._zero_state = State(0)
        self._counter = 1
        self._finalized = False
        self.index: List[Collection] = []

    def add(self, tokens: Collection[Any]):
        if self._finalized:
            raise ValueError("TokenTree has been finalized. No more tokens additions allowed")

        if len(tokens) <= 0:
            return

        self.index.append(tokens)

        current_state = self._zero_state
        for token in tokens:
            if token in current_state.transitions:
                current_state = current_state.transitions.get(token)

            else:
                next_state = State(identifier=self._counter, parent=current_state, token=token)
                self._counter += 1
                current_state.transitions[token] = next_state
                current_state = next_state

        current_state.success = True
        current_state.matched_tokens = tokens
        current_state.matched_tokens_index = len(self.index)

    def search(self, tokens: Collection[Any], return_indices: bool = False) -> List[Tuple[Collection[Any], int]]:
        return list(self.search_all(tokens, return_indices=return_indices))

    def search_one(self, tokens: Collection[Any], return_index: bool = False) -> Optional[Tuple[Collection[Any], int]]:
        result_gen = self.search_all(tokens, return_indices=return_index)

        try:
            return next(result_gen)

        except StopIteration:
            return None

    def search_all(self, tokens: Collection[Any], return_indices: bool = False) -> Generator[Tuple[Collection[Any], int], None, None]:
        if not self._finalized:
            raise ValueError("TokenTree has not been finalized. No search allowed")

        zero_state = self._zero_state
        current_state = zero_state
        for idx, token in enumerate(tokens):
            current_state = current_state.transitions.get(token, zero_state.transitions.get(token, zero_state))
            state = current_state
            while state is not zero_state:
                if state.success:
                    found_tokens = state.matched_tokens

                    if return_indices:
                        result = state.matched_tokens_index

                    else:
                        result = found_tokens

                    yield result, idx + 1 - len(found_tokens)

                state = state.longest_strict_suffix

    def finalize(self) -> None:
        if self._finalized:
            raise ValueError("TokenTree has already been finalized.")

        self._zero_state.longest_strict_suffix = self._zero_state
        self.search_lss_for_children(self._zero_state)
        self._finalized = True

    def search_lss_for_children(self, zero_state: State) -> None:
        processed = set()
        to_process = [zero_state]

        while to_process:
            state = to_process.pop()
            processed.add(state.identifier)

            for child in state.transitions.values():
                if child.identifier not in processed:
                    self.search_lss(child)
                    to_process.append(child)

    def search_lss(self, state: State) -> None:
        zero_state = self._zero_state
        parent = state.parent
        if parent is None:
            return

        traversed = parent.longest_strict_suffix

        while True:
            if state.token in traversed.transitions and traversed.transitions[state.token] is not state:
                state.longest_strict_suffix = traversed.transitions[state.token]
                break

            elif traversed is zero_state:
                state.longest_strict_suffix = zero_state
                break

            else:
                traversed = traversed.longest_strict_suffix

        suffix = state.longest_strict_suffix
        if suffix is None:
            return

        if suffix is zero_state:
            return

        if suffix.longest_strict_suffix is None:
            self.search_lss(suffix)

        for token, next_state in suffix.transitions.items():
            if token not in state.transitions:
                state.transitions[token] = next_state
