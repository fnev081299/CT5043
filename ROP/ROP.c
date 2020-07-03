// sets an array of char that is 128 long
void function_exploitable()
{
	char buf[128];
	read(0, buf, 256); //reading into the buffer
}

// main function
int main(int argc, char **argv)
{
	// runs exploitable function
	function_exploitable();
	// prints expliot
	printf("\n Expliot");
}
