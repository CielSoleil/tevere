package main

import (
	"flag"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strings"
)

func download(url string, destination string) error {
	client := &http.Client{}
	req, _ := http.NewRequest("GET", url, nil)

	// Custom headers
	req.Header.Set("user-agent", "Mozilla/5.0")
	req.Header.Set("accept", "*/*")
	req.Header.Set("origin", "https://tver.jp")
	req.Header.Set("referer", "https://tver.jp")
	req.Header.Set("x-tver-platform-type", "web")

	// Get the data
	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	// Save to file
	out, err := os.Create(destination)
	if err != nil {
		return err
	}
	defer out.Close()

	_, err = io.Copy(out, resp.Body)
	return err
}

func main() {
	episode := flag.String("episode", "", "The TVer episode url.")
	save := flag.Bool("download", false, "If passed, download the json file")
	dest := flag.String("dest", os.Getenv("HOME"), "Where will the file be saved to")
	flag.Parse()
	// The above should contain this: https://tver.jp/episodes/eps7hpk6h7

	sep := strings.Split(*episode, "/")
	slug := sep[len(sep)-1]
	log.Println("Episode slug:", slug)

	const tver string = "https://contents-api.tver.jp/contents/api/v1/episodes/"
	var apiUrl string
	var destination string

	if *save {
		// log.Println("Downloading", slug, "to file")
		apiUrl = fmt.Sprintf("%s%s", tver, slug)
		log.Println("Fetching", apiUrl)

		destination = fmt.Sprintf("%s/%s.json", *dest, slug)
		log.Println("File will be saved to:", destination)
		download(apiUrl, destination)
	}
}
