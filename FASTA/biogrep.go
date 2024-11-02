package main

import (
	"bufio"
	"errors"
	"fmt"
	"io"
	"os"
	"strings"
)

func getQueries() []string {
	queries, err := os.ReadFile(os.Args[1])
	if err != nil {
		if errors.Is(err, os.ErrNotExist) { //query in argv
			return []string{os.Args[1]}
		}
		fmt.Fprintf(os.Stderr, "An error occured reading %s\n", os.Args[1])
		os.Exit(1)
	}
	return strings.Split(strings.TrimSpace(string(queries)), "\n") //queries in file
}

func getFileHandle(filepath string) *os.File {
	fHandle, err := os.Open(filepath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "An error occured reading %s\n", filepath)
		os.Exit(1)
	}
	return fHandle
}

func someQueryInLine(queries []string, line string) bool {
	for _, query := range queries {
		if strings.Contains(line, query) {
			return true
		}
	}
	return false
}

func printSeqs(filename string, queries []string) {
	fHandle := getFileHandle(filename)
	defer fHandle.Close()
	fileReader := bufio.NewReader(fHandle)

	var printLIne bool
	for {
		line, err := fileReader.ReadString('\n')
		if err != nil {
			if err == io.EOF {
				break
			} else {
				fmt.Fprintf(os.Stderr, "An error occured reading %s\n", filename)
				os.Exit(1)
			}
		}
		if strings.HasPrefix(line, ">") {
			printLIne = someQueryInLine(queries, line)
		}
		if printLIne {
			fmt.Print(line)
		}
	}
}

func main() {
	if len(os.Args) < 3 {
		fmt.Println("usage:\n  biogrep query/queries_file fasta_files")
		os.Exit(0)
	}
	queries := getQueries()
	files := os.Args[2:]
	for _, file := range files {
		printSeqs(file, queries)
	}
}
