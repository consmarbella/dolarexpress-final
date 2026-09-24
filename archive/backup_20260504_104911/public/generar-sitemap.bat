@echo off
setlocal enabledelayedexpansion

set BASE_URL=https://dolarexpress.cl

echo ^<?xml version="1.0" encoding="UTF-8"?^> > sitemap.xml
echo ^<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"^> >> sitemap.xml

for %%f in (*.html) do (
    echo   ^<url^> >> sitemap.xml
    echo     ^<loc^>%BASE_URL%/%%f^</loc^> >> sitemap.xml
    echo     ^<lastmod^>%date:~6,4%-%date:~3,2%-%date:~0,2%^</lastmod^> >> sitemap.xml
    echo     ^<priority^>0.8^</priority^> >> sitemap.xml
    echo   ^</url^> >> sitemap.xml
)

echo ^</urlset^> >> sitemap.xml

echo Sitemap generado correctamente.
pause
