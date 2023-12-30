import time, os, sys, transpositionEncrypt, transpositionDecrypt



def main():

 inputFilename = 'C:/Users/chimu/OneDrive/Desktop/Desktop/Major_Project/WhatsLyzer_minor_project/ddmmyyyyWhatsApp Chat with BDA B _ E.txt'

  # BE CAREFUL! If a file with the outputFilename name already exists,

    # this program will overwrite that file.

 outputFilename = 'C:/Users/chimu/OneDrive/Desktop/Desktop/Major_Project/WhatsLyzer_minor_project/ddmmyyyyWhatsApp Chat with BDA B _ E.txt'
 myKey = 10

 myMode = 'encrypt' # set to 'encrypt' or 'decrypt'

  # If the input file does not exist, then the program terminates early.

 if not os.path.exists(inputFilename):



  print('The file %s does not exist. Quitting...' % (inputFilename))

  sys.exit()





if os.path.exists(outputFilename):


print('This will overwrite the file %s. (C)ontinue or (Q)uit?' % (outputFilename))

response = input('> ')

if not response.lower().startswith('c'):

     sys.exit()



     fileObj = open(inputFilename)

     content = fileObj.read()

     fileObj.close(print('%sing...' % (myMode.title()))
     startTime = time.time()
     if myMode == 'encrypt':

        translated = transpositionEncrypt.encryptMessage(myKey, content)

elif myMode == 'decrypt':
    translated = transpositionDecrypt.decryptMessage(myKey, content)


    totalTime = round(time.time() - startTime, 2)

    print('%sion time: %s seconds' % (myMode.title(), totalTime))

      # Write out the translated message to the output file.

    outputFileObj = open(outputFilename, 'w')

    outputFileObj.write(translated)

    outputFileObj.close()


    print('Done %sing %s (%s characters).' % (myMode, inputFilename, len(content)))

    print('%sed file is %s.' % (myMode.title(), outputFilename))


# If transpositionCipherFile.py is run (instead of imported as a module)
# call the main() function.

# if __name__ == '__main__':
#
#     main()