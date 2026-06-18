using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;

namespace Common
{
    public static class DataLoader
    {
        public static List<string> LoadData(string path)
        {
            var data = new List<string>();

            if (Directory.Exists(path))
            {
                foreach (var file in Directory.GetFiles(path))
                {
                    data.Add(File.ReadAllText(file));
                }
            }
            else if (path.EndsWith(".jsonl"))
            {
                foreach (var line in File.ReadLines(path))
                {
                    using (JsonDocument doc = JsonDocument.Parse(line))
                    {
                        data.Add(doc.RootElement.GetProperty("payload").GetString());
                    }
                }
            }
            else if (path.EndsWith(".csv"))
            {
                var lines = File.ReadAllLines(path);
                for (int i = 1; i < lines.Length; i++) // skip header
                {
                    data.Add(lines[i]);
                }
            }

            return data;
        }
    }
}
