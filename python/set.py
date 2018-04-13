# Set = elementi unici, non ordinati

nums = {10, 20, 30, 40};  # nuovo set di 4 elementi
print(nums);
fnums = frozenset(nums);  # nuovo frozenset a partire dal set nums
print(fnums);

print(set('abracadabra'));  # trova l'insieme di lettere nella stringa 'abracadabra'

nums.add(13);
nums.remove(20);
nums.discard(33);
nums.pop();

print({1, 2, 3}.isdisjoint({4, 5, 6}));