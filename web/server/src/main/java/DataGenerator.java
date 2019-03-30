import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVRecord;

import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;
import java.util.HashMap;

public class DataGenerator extends Thread {

    private final long timeInterval;
    private Reader reader;
    private final String file;
    private HashMap<String, String> data = new HashMap<String, String>();

    public static enum Headers{
        ID,STN,YYYYMMDD,HH,DD,FH,FF,FX,T,T10,TD,SQ,Q,DR,RH,P,VV,N,U,WW,IX,M,R,S,O,Y
    }


    DataGenerator(String csvfile, long timer){
        this.file = csvfile;
        this.timeInterval = timer;
    }

    // TODO: Read a file from an url

    public void read() throws IOException {
        System.out.println("About to read the csv file");
        // Lazy-loading
        reader = new FileReader(this.file);
        Iterable<CSVRecord> records = CSVFormat.RFC4180.withFirstRecordAsHeader().parse(this.reader);
        for (CSVRecord record : records) {
            try {

                data.put(Headers.ID.toString() , record.get(Headers.ID));
                data.put(Headers.YYYYMMDD.toString() , record.get(Headers.YYYYMMDD));
                data.put(Headers.HH.toString() , record.get(Headers.HH));
                data.put(Headers.DD.toString() , record.get(Headers.DD));
                data.put(Headers.FH.toString() , record.get(Headers.FH));
                data.put(Headers.T.toString() , record.get(Headers.T));
                data.put(Headers.SQ.toString() , record.get(Headers.SQ));
                data.put(Headers.P.toString() , record.get(Headers.P));
                data.put(Headers.VV.toString() , record.get(Headers.VV));
                data.put(Headers.U.toString() , record.get(Headers.U));
                Thread.sleep(timeInterval);
                //System.out.println("debug: " + data);

            } catch (InterruptedException e)
            {
                e.printStackTrace();
            }

        }
    }

    @Override
    public void run() {
        try {
            read();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public HashMap<String, String> getData() {
        return data;
    }

}
