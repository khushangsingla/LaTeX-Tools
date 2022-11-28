# Algorithm Writer

This tool can be used to convert algorithm to code of $\LaTeX$.
To use this, run `algo.py` using the command `python3 algo.py sample.algo` where sample.algo is the file containing algorithm.

This tool writes the $\LaTeX$ tool according to crlscode3e

### Example
Here is an example algorithm
```
proc test-algo(A, B)
    for j <- 2 to A.length do
	// Insert $A[j]$ into $A[1 .. j-1]$
        key <- A[j] 
        i <- j - 1
        while i > 0 and A[i] > key do
            A[i+1] <- A[i]
            i <- i - 1
        end
        A[i+1] <- key
    end
    if x == 3 then do
        {{Do nothing}}
    end
end
```

Using this tool, this can be converted to $\LaTeX$ code. The result for the above algorithm as given by the tool is:

```
\begin{codebox}
\Procname{\proc{test-algo}(\id{A}, \id{B})}
\zi    \For \id{j} $\leftarrow$ 2 \To \attrib{A}{length} \Do
\zi	\Comment  Insert \id{A}[\id{j}] into \id{A}[1 $\twodots$ \id{j}$-$1]
\zi        \id{key} $\leftarrow$ \id{A}[\id{j}]
\zi        \id{i} $\leftarrow$ \id{j} $-$ 1
\zi        \While \id{i} $>$ 0 \id{and} \id{A}[\id{i}] $>$ \id{key} \Do
\zi            \id{A}[\id{i}$+$1] $\leftarrow$ \id{A}[\id{i}]
\zi            \id{i} $\leftarrow$ \id{i} $-$ 1
\zi        \End
\zi        \id{A}[\id{i}$+$1] $\leftarrow$ \id{key}
\zi    \End
\zi    \If \id{x} $\isequal$ 3 \Then \Do
\zi        {{\id{Do} \id{nothing}}}
\zi    \End
\zi\End
\end{codebox}
```
