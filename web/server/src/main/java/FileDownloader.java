import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.nio.file.*;

public class FileDownloader {

    private final String url;
    private final String filepath;


    public FileDownloader(String url, String filepath){
        this.url = url;
        Path file = Paths.get("../resources/").toAbsolutePath();
        this.filepath = filepath;
        System.out.println("*** " + filepath);
    }

    public FileDownloader(String url, String filepath, String ext){
        this.url = url;
        this.filepath = filepath + ext;
    }

    public void download() throws IOException {
        System.out.println("About to download the file located at " + url);
        InputStream inputStream = new URL(url).openStream();
        Files.copy(inputStream, Paths.get(filepath), StandardCopyOption.REPLACE_EXISTING);
    }

}
