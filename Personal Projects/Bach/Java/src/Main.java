import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        Scanner readin = null;
        try {
            readin = new Scanner(System.in);
            Integer input = 0;
            System.out.print("Enter a number: ");
            try {
                input = readin.nextInt();

                if (input < 0) System.out.print("Hmm, I'm not that smart to deal with negative numbers. Try positive and zero next time.");
                else
                {
                    int output = 0;
                    int out_length = 0; // Number of digits output has.
                    while (input != 0) {
                        int digit = input % 10 + 1; // Get the last number and plus 1.
                        output = digit * (int) Math.pow(10, out_length) + output;
                        if (digit == 10) out_length += 2;
                        else out_length++;
                        if (out_length > 10) break; // Integer.MAX_VALUE is roughly around 2 bil, which has 10 digits in total.

                        input /= 10; // Remove the last digit.
                    }

                    if (output < 0 || out_length > 10) System.out.print("Hmm, seems like the number generated exceeded " + input.MAX_VALUE + ".");

                    System.out.println("Output: " + output);
                }
            }
            catch (java.util.InputMismatchException ime) {
                System.out.print("Hmm, maybe you typed in a string, or you type the number too big. Try typing an int in the range ");
                System.out.print(input.MAX_VALUE + " and " + input.MIN_VALUE + " next time.");
            }
        }
        finally {
            readin.close();
        }

    }
}
