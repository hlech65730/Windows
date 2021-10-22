#include <stdlib.h>
#include <stdio.h>
#include <windows.h>

int main()
{int c,n,m;
 srand( (unsigned) time(NULL) ) ;
	printf("random pw\n");
	for (m=1;m<=10;m++)
	{ printf(" \n");
        for(c=1;c<=10;c++)
            {
                n = rand()%100+33;
                printf("%c",n);
            }
	  printf(" \n");
	}
	return 0;
}
