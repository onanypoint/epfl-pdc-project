# Text transfert over audio channel
Project for the 2015 [Principles of Digital Communications](http://ipg.epfl.ch/page-136504-en.html) class taught by Prof. Emere Telatar at the [Swiss Federal Institute of Technology in Lausanne](https://epfl.ch/) (EPFL) in Switzerland.

## Assignment
Develop a proof of concept to show that we can exchange files “over the air” between two laptops, by using the speaker of one laptop as the transmitting device and the microphone of the other laptop as the receiving device in presence of an interfering third party.

## Setup
The project requires pyaudio, it can be installed via ```pip install``` after the prerequisite portaudio library has been installed. 

On OSX using Homebrew:

	brew install portaudio 
	pip install pyaudio

To run the project use the makefile:

	# Install dependencies
	make init
	
	# Run the tests
	make test
	
	# Run the transmitter by reading a "message.txt" file
	make transmitter
	
	# Run the receiver
	make receiver

### Notebook
A [jupyter notebook](http://jupyter.org/) going through the whole pipeline is available. It even has plots :)


#### References
- [Applidium : Data transfer](http://applidium.com/en/news/data_transfer_through_sound/)
- [Minimodem : audio communication](http://www.whence.com/minimodem/)
- [GnuRadio](http://gnuradio.org/redmine/projects/gnuradio/wiki)
- [Fsk explained with python](http://www.allaboutcircuits.com/technical-articles/fsk-explained-with-python/) by Travis Fagerness
- [Frame synchronization in digital communication systems](https://jyyuan.wordpress.com/2014/02/01/frame-synchronization-in-digital-communication-systems/)
- [Phase shift keying](http://en.wikipedia.org/wiki/Phase-shift_keying#Example:_Differentially_encoded_BPSK)
- [Barker Code](http://en.wikipedia.org/wiki/Barker_code)
- [Differential coding](https://en.wikipedia.org/wiki/Differential_coding)
- [Forward error correction](https://en.wikipedia.org/wiki/Forward_error_correction)


