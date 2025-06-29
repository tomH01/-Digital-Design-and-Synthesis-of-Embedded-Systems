#include "ap_int.h"

#define N 2
#define M 4

typedef ap_int<M * 8> block_t;
typedef ap_int<M * N * 8> message_t;

block_t encrypt_decrypt_block(block_t block, block_t key) {
  return block ^ key;
} 

message_t n_block_cbc(bool encrypt_decrypt, message_t message, block_t key) {
  block_t prev_block = key;
  message_t output = 0;

  int upper, lower;
  block_t curr_block, xored_block;

  for (int i = 0; i < N; i++) {
    // Start of message at MSB
    upper = (N - i) * M * 8 - 1;
    lower = (N - i - 1) * M * 8;

    curr_block = message.range(upper, lower);

    #pragma HLS inline
    xored_block = encrypt_decrypt_block(curr_block, prev_block);

    // Encryption / Decryption
    prev_block = encrypt_decrypt ? xored_block : curr_block;

    output.range(upper, lower) = xored_block;
  } 

  return output;
} 

