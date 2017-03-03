#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <sys/time.h>

int main(int argc,char **argv){

  struct timeval stop, start;

  gettimeofday(&start, NULL);

  int j;
  for (int i=0;i<1999999999;i++){
  	j = 5;
  }

  gettimeofday(&stop, NULL);
  printf("process %d took %lu\n", atoi(argv[1]), stop.tv_sec - start.tv_sec);

  return 0;


}