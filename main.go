package main

import (
   "bufio"
   "encoding/json"
   "flag"
   "fmt"
   "github.com/dan-locke/language-model-retrieval/index"
   "io/ioutil"
   "os"
   "path"
   "path/filepath"
   "strconv"
   "strings"
   "unicode"
   // _ "net/http/pprof"
   // "runtime"
   // "runtime/pprof"
   // "log"
)

func makeId(s string) string {
   _, f := path.Split(s)
   parts := strings.Split(f, ".")
   if strings.Contains(parts[0], "-") {
      parts = strings.Split(parts[0], "-")
   } else {
      f = parts[0]
      parts = []string{}
      curr := true
      start := 0
      tLen := len(f)
      for i := 0; i < tLen; i++ {
         past := curr
         if unicode.IsDigit(rune(f[i])) {
            curr = true
         } else {
            curr = false
         }
         if curr != past {
            parts = append(parts, f[start:i])
            start = i
         }
         if i+1 == tLen {
            parts = append(parts, f[start:i+1])
         }
      }
   }
   for i := range parts {
      num, err := strconv.Atoi(parts[i])
      if err == nil {
         parts[i] = fmt.Sprintf("%d", num)
      }
   }
   return strings.Join(parts, "")
}

// load stopwords to map
func getStopwords(path string) (map[string]int, error) {
   f, err := os.Open(path)
   defer f.Close()
   if err != nil {
      return nil, err
   }
   scanner := bufio.NewScanner(f)
   m := map[string]int{}
   for scanner.Scan() {
      m[strings.TrimSpace(scanner.Text())] = 1
   }
   if err := scanner.Err(); err != nil {
      return nil, err
   }
   return m, err
}

//script for indexing ussc and sigir collections
func main() {
   filesPath := flag.String("p", "", "Path to files to index.")
   indName := flag.String("i", "", "Index name.")
   field := flag.String("f", "flattened_text", "JSON field to index.")
   paras := flag.Bool("b", false, "Split Australian into paragraphs")
   stopwordsPath := flag.String("s", "", "Path to stopwords file.")
   flag.Parse()
   var err error
   if *filesPath == "" {
      fmt.Println("Please specify path to files to index.")
      return
   }
   if *indName == "" {
      fmt.Println("Please specify index name.")
      return
   }
   stopwords := map[string]int{}
   if *stopwordsPath != "" {
      stopwords, err = getStopwords(*stopwordsPath)
      if err != nil {
         panic(err)
      }
   }
   // f, err := os.Create("memprofile.prof")
   // if err != nil {
   //     log.Fatal("could not create memory profile: ", err)
   // }
   // defer f.Close()
   // runtime.GC()
   ind, err := index.NewIndex(*indName)
   if err != nil {
      panic(err)
   }
   ind.AddField("text", index.DefaultTermScoringModel, index.DefaultScoringMethod, "html_tokenizer", true, true, stopwords)
   err = filepath.Walk(*filesPath, func(path string, info os.FileInfo, err error) error {
      if err != nil {
         return err
      }
      if strings.Contains(info.Name(), ".json") {
         // open file and index
         buff, err := ioutil.ReadFile(path)
         if err != nil {
            return err
         }
         var v map[string]interface{}
         err = json.Unmarshal(buff, &v)
         if err != nil {
            return err
         }
         fmt.Printf("%s\n", path)
         if *field == "html" || *field =="html_with_citations" {
            fld := v[*field].(string)
            if fld != "" {
               ind.IndexDoc(map[string]string{"text": fld}, fmt.Sprintf("%1.f", v["id"].(float64)))
               // if err := pprof.WriteHeapProfile(f); err != nil {
               //     panic(err)
               // }
            }
         } else {
            _id := makeId(info.Name())
            if *paras {
               bodyParas := v["body"].([]interface{})
               for i := range bodyParas {
                  bp := bodyParas[i].(map[string]interface{})
                  ind.IndexDoc(map[string]string{"text": bp["text"].(string)}, _id+fmt.Sprintf("-%d", int(bp["pos"].(float64))))
               }
            } else if *field == "header" {
               headnoteParas := v["header"].([]interface{})
               var comb string
               for i := range headnoteParas {
                  comp := headnoteParas[i].(map[string]interface{})
                  if strings.Contains(strings.ToLower(comp["tag"].(string)), "") {
                     comb = comp["text"].(string)
                     break
                  } else {
                     comb += comp["text"].(string) + " "
                  }
               }
               ind.IndexDoc(map[string]string{"text": comb}, _id)
            } else {
               fld := v[*field].(string)
               if fld != "" {
                  ind.IndexDoc(map[string]string{"text": fld}, _id)
               }
            }
         }
      }
      return nil
   })
   if err != nil {
      panic(err)
   }
   err = ind.Save()
   if err != nil {
      panic(err)
   }
}