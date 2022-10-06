# SWEN 5432 IEEE 754 Calculator

import PySimpleGUI as sg
import sys
import os

def DecToBin(input):
	if float(input) == 0.0:
		return '0', '00000000', '00000000000000000000000'
	if float(input) < 0:
		sign = '1'
	else:
		sign = '0'
	n, f = divmod(abs(float(input)), 1)

	# integer part
	b = ''
	while(n > 0):
		d=n%2
		b = str(d)[0:1] + b
		n=n//2
	if b == '':
		bin_intgr = '0'
	else:
		bin_intgr = b

	# fractional part
	b = ''
	while(True):
		i, f = divmod(f * 2, 1)
		b += str(int(i))
		if f == 0:
			break
	if b == '':
		b = 0
	else:
		bin_frac = b

	# exponent	
	tmp = (bin_intgr + '.' + bin_frac).lstrip('0')
	if tmp.find('.') < tmp.find('1'):
		exp_un = tmp.find('1') * -1
	else:
		exp_un = tmp.find('.') - tmp.find('1') - 1
	#print(exp_un)
	if exp_un <= -126 or exp_un >= 127:
		return 'NaN', 'NaN', 'NaN'
	exp = str(bin(exp_un + 127))[2:].rjust(8, '0')

	# mantissa
	if (exp_un >= 0):
		man = (tmp.replace('.',''))[1:24].ljust(23,'0')
	else:
		man = (tmp[tmp.find('1'):])[1:24]
	return sign, exp, man

def BinToDec(sign, exp, mantissa):
	if exp == '11111111':
		if sign == '1' and int(mantissa) == 0:
			return '-Infinity'
		elif sign == '0' and int(mantissa) == 0:
			return '+Infinity'
		else:
			return 'NaN'
	try:
		x = int(sign)
		if x < 0 or x > 1:
			return 'Nan'
	except:
		return 'NaN'
	try:
		int(exp, 2)
	except:
		return 'NaN'
	try:
		int(mantissa, 2)
	except:
		return 'NaN'
	if int(sign) + int(exp) + int(mantissa) == 0:
		return 0
	sign = sign[0:1]
	exp = exp.ljust(8, '0')
	mantissa = mantissa.ljust(23, '0')
	exp = exp[::-1]
	ex = 0
	for i, x in enumerate(exp):
		if x == '1':
			ex = ex + (2 ** int(i))
	ma = 0
	for i, x in enumerate(mantissa):
		if x == '1':
			# print (int(i) * -1)
			ma = ma + (2 ** ((i + 1) * -1))
	if sign == '1':
		ma += 1
		basenumber = (-1 * (ma * (2 ** (ex - 127))))
	elif sign == '0':
		ma += 1
		basenumber  = (ma * (2 ** (ex - 127)))
	return '{:e}'.format(basenumber)

def BinToHex(sign, exp, mantissa):
	try:
		int(sign)
		int(exp)
		int(mantissa)
	except:
		return
	try:
		x = int(sign)
		if x < 0 or x > 1:
			return 'Nan'
	except:
		return 'NaN'
	try:
		int(exp, 2)
	except:
		return 'NaN'
	try:
		int(mantissa, 2)
	except:
		return 'NaN'
	sign = sign[0:1]
	exp = exp.ljust(8, '0')
	mantissa = mantissa.ljust(23, '0')
	bin = sign + exp + mantissa
	return str(hex(int(bin[0:4], 2)))[2] + str(hex(int(bin[4:8], 2)))[2] + str(hex(int(bin[8:12], 2)))[2] + str(hex(int(bin[12:16], 2)))[2] + str(hex(int(bin[16:20], 2)))[2] + str(hex(int(bin[20:24], 2)))[2] + str(hex(int(bin[24:28], 2)))[2] + str(hex(int(bin[28:], 2)))[2]

def HexToBin(data):
	if data == '':
		return 
	try:
		out = ''
		for x in data:
			out = out + str(bin(int(x,16)))[2:].rjust(4, '0')
		return out[0:1], out[1:9].ljust(8,'0'),out[9:].ljust(23,'0')
	except:
		return 'NaN', 'NaN', 'NaN'

sg.theme('DarkBlue')

number1_column = [
	[
		sg.Button('A', size=(5, 3), button_color='lightblue'),
		sg.Button('7', size=(5, 3)),
		sg.Button('8', size=(5, 3)),
		sg.Button('9', size=(5, 3)),
		sg.Button('*', size=(5, 3), button_color='lightgreen'),
        sg.Text('Normalization                ', size =(None, None)),
		sg.InputText(key='_Normalization_', size=(25, 3), disabled=True, text_color='black')
	]]

number2_column = [
	[
		sg.Button('B', size=(5, 3), button_color='lightblue'),
		sg.Button('4', size=(5, 3)),
		sg.Button('5', size=(5, 3)),
		sg.Button('6', size=(5, 3)),
		sg.Button('-', size=(5, 3), button_color='lightgreen'),
        sg.Text('Decimal                        ', size =(None, None)), 
		sg.InputText(key='_DEC_', size=(25, 3), disabled=True, text_color='black')
	]]

number3_column = [
	[
		sg.Button('C', size=(5, 3), button_color='lightblue'),
		sg.Button('1', size=(5, 3)),
		sg.Button('2', size=(5, 3)),
		sg.Button('3', size=(5, 3)),
		sg.Button('+', size=(5, 3), button_color='lightgreen'),
        sg.Text('Hexadecimal                 ', size=(None, None)), 
		sg.InputText(key='_HEX_', size=(25, 3), disabled=True, text_color='black')
	]]
	
number4_column = [
	[
		sg.Button('D', size=(5, 3), button_color='lightblue'),
		sg.Button('±', size=(5, 3)),
		sg.Button('0', size=(5, 3)),
		sg.Button('.', size=(5, 3), font=(sg.DEFAULT_FONT, 10, 'bold')),
		sg.Button('=', size=(5, 3), button_color='lightgreen'),
        sg.Text('Sign                             ',size=(None, None)),
        sg.InputText(key='_SIGN_', size=(25, 3), disabled=True, text_color='black')
	]]

number5_column = [
	[
		sg.Button('E', size=(5, 3), button_color='lightblue'),
		sg.Button('d2b', size = (7, 3), button_color='red'),
		sg.Button('d2h', size = (7, 3), button_color='red'),
		sg.Button('b2d', size = (8, 3), button_color='green'),
        sg.Text('Exponent                       ',size=(None, None)),
        sg.InputText(key='_EXPONENT_', size=(25, 3), disabled=True, text_color='black')
	]]

final_column = [
	[
		sg.Button('F', size=(5, 3), button_color='lightblue'),
		sg.Button('h2d', size = (7, 3), button_color='yellow'),
		sg.Button('h2b', size = (7, 3), button_color='yellow'),
		sg.Button('b2h', size = (8, 3), button_color='green'),
        sg.Text('Mantissa                       ',size=(None, None)),
        sg.InputText(key='_MANTISSA_', size=(25, 3), disabled=True, text_color='black')
	]]

clear_column = [
	[
		sg.Button('Help', size=(9, 3), button_color='gray'),
		sg.Button('Clear', size=(23, 3)),
		sg.Radio('Dec', 'base', key='_decimal_', default=True),
		sg.Radio('Bin', 'base', key='_binary_'),
		sg.Radio('Hex', 'base', key='_hexadecimal_'),
        sg.Text('                                       ',size=(None, None)),
	]]

layout = [
	[sg.Text('Team RamRod.')],
	[sg.Output(size=(90, 12), key='_OUT_')],
	[sg.Column(clear_column)],
	[sg.Column(number1_column)],
	[sg.Column(number2_column)],
	[sg.Column(number3_column)],
	[sg.Column(number4_column)],
	[sg.Column(number5_column)],
	[sg.Column(final_column)]
	]

def NormalizeHex(input):
	return input.ljust(8,'0')
	
def NormalizeBin(sign, exp, mantissa):
	return sign[0:1], exp.ljust(8, '0'), mantissa.ljust(23, '0')

def ClearWindows():
	window['_DEC_'].Update('')
	window['_HEX_'].Update('')
	window['_SIGN_'].Update('')
	window['_EXPONENT_'].Update('')
	window['_MANTISSA_'].Update('')
	window['_Normalization_'].Update('')
	window['_OUT_'].Update('')

def DisplayError():
	window['_DEC_'].Update('NaN')
	window['_HEX_'].Update('NaN')
	window['_SIGN_'].Update('NaN')
	window['_EXPONENT_'].Update('NaN')
	window['_MANTISSA_'].Update('NaN')
	window['_Normalization_'].Update('NaN')
	print('NaN')

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

window = sg.Window('IEEE 754 Calculator', layout, element_justification='c', icon=resource_path('Calculator.ico'))
# uses relative path for the icon to accommodate pyinstaller

while True:
	event, values = window.read()
	
	# End program if user closes window or
	# presses the OK button
	if event == sg.WIN_CLOSED: break

	# Handle input events
	try:
		int(event)
		if values['_decimal_'] == True:
			window['_DEC_'].Update(values['_DEC_'] + event)
		elif values['_binary_'] == True and (event == '0' or event == '1'):
			if len(values['_SIGN_']) == 0:
				window['_SIGN_'].Update(event)
			
			if len(values['_SIGN_']) == 1 and len(values['_EXPONENT_']) < 8:
				window['_EXPONENT_'].Update(values['_EXPONENT_'] + event)
			
			if len(values['_SIGN_']) == 1 and len(values['_EXPONENT_']) == 8 and len(values['_MANTISSA_']) < 23:
				window['_MANTISSA_'].Update(values['_MANTISSA_'] + event)
	except:
		pass

	if event.isnumeric and values['_hexadecimal_'] == True and len(values['_HEX_']) < 8:
		window['_HEX_'].Update(values['_HEX_'] + event)

	if event == '.': 
		if values['_decimal_'] == True and values['_DEC_'].find('.') == -1:
			window['_DEC_'].Update(values['_DEC_'] + '.')

	if event == '±': 
		try:
			if values['_DEC_'][0:1] == '-': window['_DEC_'].Update(values['_DEC_'][1:])
		except:
			window['_DEC_'].Update('')

	if event == '±': 
		if values['_DEC_'][0:1] != '-': window['_DEC_'].Update('-' + values['_DEC_'])
	
	if event == 'd2b':
		try:
			s, e, m = DecToBin(float(values['_DEC_']))
			window['_SIGN_'].Update(s)
			window['_EXPONENT_'].Update(e)
			window['_MANTISSA_'].Update(m)
			if int(e) == 0 and int(m) != 0:
				window['_Normalization_'].Update('Denormalized')
			else:
				window['_Normalization_'].Update('Normalized')
		except:
			pass
	if event == 'd2h':
		try:
			S, E, M = DecToBin(values['_DEC_'])
			window['_HEX_'].Update(BinToHex(str(S), str(E), str(M)))
			if int(E) == 0 and int(M) != 0:
				window['_Normalization_'].Update('Denormalized')
			else:
				window['_Normalization_'].Update('Normalized')
		except:
			pass
	if event == 'b2d':
		try:
			int(values['_SIGN_'])
			int(values['_EXPONENT_'])
			int(values['_MANTISSA_'])
			window['_DEC_'].Update(BinToDec(values['_SIGN_'], values['_EXPONENT_'],values['_MANTISSA_']))
			if int(values['_EXPONENT_']) == 0 and int(values['_MANTISSA_']) != 0:
				window['_Normalization_'].Update('Denormalized')
			else:
				window['_Normalization_'].Update('Normalized')
		except:
			pass
	if event == 'b2h':
		try:
			window['_HEX_'].Update(BinToHex(values['_SIGN_'], values['_EXPONENT_'],values['_MANTISSA_']))
			if int(values['_EXPONENT_']) == 0 and int(values['_MANTISSA_']) != 0:
				window['_Normalization_'].Update('Denormalized')
			else:
				window['_Normalization_'].Update('Normalized')
		except:
			pass
	if event == 'h2b':
		try:
			S, E, M = HexToBin(values['_HEX_'])
			window['_SIGN_'].Update(S)
			window['_EXPONENT_'].Update(E)
			window['_MANTISSA_'].Update(M)
		except:
			pass
	if event == 'h2d':
		try:
			S, E, M = HexToBin(values['_HEX_'])
			window['_DEC_'].Update(BinToDec(S, E, M))
		except:
			pass
	if event == 'Clear':
		ClearWindows()
	if event == '+':
		try:
			operation = '+'
			operand1 = values['_DEC_']
			ClearWindows()
		except:
			pass
	if event == '-':
		try:
			operand1 = values['_DEC_']
			operation = '-'
			ClearWindows()
		except:
			pass
	if event == '*':
		try:
			operand1 = values['_DEC_']
			operation = '*'
			ClearWindows()
		except:
			pass
	if event == '=':
		try:
			operand2 = values['_DEC_']
			if operation == '+':
				solution = str(float(operand1) + float(operand2))
			elif operation == '-':
				solution = str(float(operand1) - float(operand2))
			elif operation == '*':
				solution = str(float(operand1) * float(operand2))
			#window['_DEC_'].Update('{:e}'.format(float(solution)))
			window['_DEC_'].Update('{:e}'.format(float(solution)))
			S, E, M = DecToBin(solution)
			window['_HEX_'].Update(BinToHex(str(S), str(E), str(M)))
			S, E, M = DecToBin(solution)
			window['_SIGN_'].Update(S)
			window['_EXPONENT_'].Update(E)
			window['_MANTISSA_'].Update(M)

			s1, e1, m1 = DecToBin(operand1)
			s2, e2, m2 = DecToBin(operand2)
			s3, e3, m3 = DecToBin(solution)
			if int(e3) == 0 and int(m3) != 0:
				window['_Normalization_'].Update('Denormalized')
			else:
				window['_Normalization_'].Update('Normalized')		
			h1 = BinToHex(s1, e1, m1)
			h2 = BinToHex(s2, e2, m2)
			print(operand1, operation, operand2)
			print(''.ljust(80, '-'))
			print(solution)
			print()
			print(s1, e1, m1, operation, s2, e2, m2)
			print(''.ljust(80, '-'))
			print(s3, e3, m3)
			print()
			print(h1, operation, h2)
			print(''.ljust(80, '-'))
			print(BinToHex(str(S), str(E), str(M)))
		except:
			pass
	if event=='Help':
		helpInfo = 'To use:\n\nSelect Dec, Bin, or Hex to determine input type.\nThe data entry will automatically move to the correct field.\nAll calculations are done in decimal, so \nenter whatever data type you wish, then hit the appropriate conversion button for\nthat base to decimal.'
		sg.Popup(helpInfo, no_titlebar=True, background_color='gray', text_color='black', button_type='POPUP_BUTTONS_OK', keep_on_top=True )
		
window.close()
