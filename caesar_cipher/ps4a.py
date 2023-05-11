# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    '''
    
    if len(sequence) == 1:
        return [sequence]
    else: 
        # get the permutations for sequence[1:]
        l_old = get_permutations(sequence[1:])
        
        # initialize new list for returning
        l_new = []
        
        # insert sequence[0] at every index and append it to the list
        for permutation in l_old:
            for j in range(len(permutation)+1):
                s = permutation[0:j] + sequence[0] + permutation[j:]
                l_new.append(s)
        return sorted(l_new)
            

if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
    # if true branch
    assert get_permutations('z') == ['z']
    
    #if false branch
    assert get_permutations('zc') == ['cz', 'zc']
    
    #if false branch with loop multiple times
    assert get_permutations('czb') == ['bcz', 'bzc', 'cbz', 'czb', 'zbc', 'zcb']

