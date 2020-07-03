#include <stdio.h>


void targetFunction()
{
/* find the target */
printf("\n Target function found!");
printf("\n Hi there!");

}

void echo()
{
	/* creates buffer */
	char buffer[20];

  	printf("Enter some text:\n");

  	/* gets the text using %s = "string" */
  	scanf("%s", buffer);

  	/* 	outputs: 
		you have entered (entry) 
		next line
		to the buffer
  	 */
  	printf("You have entered: %s\n", buffer);

}

int main()
{
/* outputs everything */
echo();
/* returns 0 */
return 0;

}
