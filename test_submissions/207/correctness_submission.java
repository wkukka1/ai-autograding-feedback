/**
 * A minimal implementation of a binary search tree storing Integers.
 * See the Python version for additional documentation; we haven't copied over any docstrings here.
 * You can also see
 * <a href="https://www.teach.cs.toronto.edu/~csc148h/notes/binary-search-trees/bst_implementation.html">CSC148 Course Notes Section 8.5 BST Implementation and Search</a>
 * if you want a refresher on BSTs, but it is not required to complete this assignment.
 */
public class BST {
    private Integer root;

    private BST left;
    private BST right;

    public BST(Integer root) {
        if (root != null) { // check to ensure we don't accidentally try to store null at the root!
            this.root = root;
            left = new BST();
            right = new BST();
        }
        // Note: each of the attributes will default to null if root == null
    }

    /**
     * Alternate constructor, so we don't have to explicitly pass in null.
     */
    public BST() {
        this(null);
    }


    // TODO Task: Implement the BST methods.

    public boolean isEmpty() {
        // Omitted assume that the implementation is correct
    }


    public void insert(Integer item) {
        // Omitted assume that the implementation is correct
    }


    public void delete(Integer item) {
        // Omitted assume that the implementation is correct
    }

    private void deleteRoot() {
        // TODO implement me! Listo
        if (this.left.isEmpty() && this.right.isEmpty()) {
            this.root = null;
            this.left = null;
            this.right = null;
        } else if (this.left.isEmpty()) {
            this.right = this.right.right;
        } else (this.right.isEmpty()) {
            this.right = this.left.right;
        }
    }

    public static void main(String[] args) {
        // Important: do not add any code to a "psvm" main method in this class,
        //            as it may prevent your code from running on MarkUs.
        //            If you want to test this code, you can either create a test file
        //            similar to the provided BSTSelfTest.java or create a main method
        //            in a local .java file which you don't push to MarkUs.
        //            In particular, if you include any code on MarkUs which calls:
        //            new Integer(x); // for any x
        //            then your code won't be able to be compiled and run, with an error
        //            similar to:
        //            "warning: [removal] Integer(int) in Integer has been deprecated and marked for removal"
    }

}
