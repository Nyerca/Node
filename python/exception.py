try:
    n = int('five')
except ValueError:
    print('Invalid number!')
	
	
def try_except_except_test(x):
	try:
		n = 5 / x
	except ZeroDivisionError as err:
		print('Invalid operation ({})!'.format(err))
	else:
		print('ok');
		
try_except_except_test(3)
try_except_except_test(0)



def div(num, den):
    if den == 0:
        # se il denominatore è 0 riporta un'eccezione
        raise ZeroDivisionError('Impossibile dividere per 0')
    return num / den
div(8, 0)