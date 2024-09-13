package main

import (
    "bufio"
    "fmt"
    "os"
    "sync"
)

// Function to process a URL
func processURL(wg *sync.WaitGroup, url string) {
    defer wg.Done()

    fmt.Println("Processing URL:", url)  // Log the URL being processed

    // Initialize the WebDriver (if using Selenium)
    wd, err := initDriver()
    if err != nil {
        fmt.Println("Error initializing driver:", err)  // Log driver initialization error
        return
    }
    defer wd.Quit()

    // Handle CAPTCHA (if needed)
    captcha, err := captureCaptchaAndSolve(wd)
    if err != nil {
        fmt.Println("Error solving CAPTCHA:", err)  // Log CAPTCHA solving error
        return
    }
    fmt.Println("Solved CAPTCHA:", captcha)  // Log solved CAPTCHA

    // Fill the form
    err = fillForm(wd, url)
    if err != nil {
        fmt.Println("Error filling form:", err)  // Log form filling error
        return
    }
    fmt.Println("Form filled for URL:", url)  // Log form filling success
}

func main() {
    // Open the URLs from the file
    file, err := os.Open("urls.txt")
    if err != nil {
        fmt.Println("Failed to open file:", err)  // Log file opening error
        return
    }
    defer file.Close()

    fmt.Println("Reading URLs from file...")

    scanner := bufio.NewScanner(file)
    var wg sync.WaitGroup

    // Process each URL in parallel
    for scanner.Scan() {
        url := scanner.Text()
        fmt.Println("Read URL:", url)  // Log each URL read from the file
        wg.Add(1)
        go processURL(&wg, url)
    }

    // Wait for all scraping processes to finish
    wg.Wait()

    if err := scanner.Err(); err != nil {
        fmt.Println("Error reading URLs:", err)  // Log URL reading error
    }
    fmt.Println("Completed processing all URLs.")  // Log completion of processing
}
