#include <stdlib.h>
#include <stdio.h>

int main()
{int c,n;
	printf("random pw\n");
	for(c=1;c<=10;c++)
	{
	n = rand()%100+33;
	printf("%c\n",n);
	}
	return 0;
}
