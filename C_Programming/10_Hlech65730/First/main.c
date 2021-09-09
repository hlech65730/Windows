#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    printf("Hello world!\n");
    char var_name[20];

    printf("Please tell me Your name :");
    scanf("%s",var_name);
    printf("Hello %s,let us be friends.\n",var_name);
    return 0;
}
