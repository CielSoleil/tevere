package main

import (
	"io"
	"net/http"
	"os"
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
