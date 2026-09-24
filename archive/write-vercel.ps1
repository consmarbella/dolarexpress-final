$json = '{"buildCommand":"vite build && node copy-html-files.js","outputDirectory":"dist","rewrites":[{"source":"/(.*)","destination":"/index.html"}]}'
Set-Content -Path 'C:\Users\matte\Desktop\repo-dolarexpress\vercel.json' -Value $json -NoNewline
