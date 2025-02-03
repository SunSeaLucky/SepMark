from . import *
from .Encoder_U import DW_Encoder
from .Decoder_U import DW_Decoder
# from .Noise import Noise
from .Random_Noise import Random_Noise


class DW_EncoderDecoder(nn.Module):
	'''
	A Sequential of Encoder_MP-Noise-Decoder

	感觉是把 Decoder_U 和 Encoder_U 合起来，方便调用
	'''

	def __init__(self, message_length, noise_layers_R, noise_layers_F, attention_encoder, attention_decoder):
		# 可以直接写成 super().__init__()，左边是 Python 3 的写法，下面是 Python 2 的写法
		super(DW_EncoderDecoder, self).__init__()
		self.encoder = DW_Encoder(message_length, attention = attention_encoder)
		self.noise = Random_Noise(noise_layers_R + noise_layers_F, len(noise_layers_R), len(noise_layers_F))
		self.decoder_C = DW_Decoder(message_length, attention = attention_decoder)
		self.decoder_RF = DW_Decoder(message_length, attention = attention_decoder)


	def forward(self, image, message, mask):
		encoded_image = self.encoder(image, message)
		noised_image_C, noised_image_R, noised_image_F = self.noise([encoded_image, image, mask])
		decoded_message_C = self.decoder_C(noised_image_C)
		decoded_message_R = self.decoder_RF(noised_image_R)
		decoded_message_F = self.decoder_RF(noised_image_F)
		return encoded_image, noised_image_C, decoded_message_C, decoded_message_R, decoded_message_F

