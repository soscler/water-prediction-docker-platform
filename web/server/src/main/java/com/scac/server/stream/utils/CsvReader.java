package com.scac.server.stream.utils;


import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVRecord;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;
import java.util.HashMap;

@Component
public class CsvReader implements Runnable{
    @Value("${timer}")
    private long timeInterval;

    private Reader reader;

    @Value("${datafile}")
    private  String file;
    private HashMap<Headers, String> data = new HashMap<Headers, String>();

    public static enum Headers{
        ID,STN,YYYYMMDD,HH,DD,FH,FF,FX,T,T10,TD,SQ,Q,DR,RH,P,VV,N,U,WW,IX,M,R,S,O,Y
    }


    // TODO: Read a file from an url

    public void read() throws IOException {
        System.out.println("About to read the csv file");
        System.out.println(file);
        // Lazy-loading
        reader = new FileReader(this.file);
        Iterable<CSVRecord> records = CSVFormat.RFC4180.withFirstRecordAsHeader().parse(this.reader);
        for (CSVRecord record : records) {
            try {

                data.put(Headers.ID , record.get(Headers.ID));
                data.put(Headers.YYYYMMDD , record.get(Headers.YYYYMMDD));
                data.put(Headers.HH , record.get(Headers.HH));
                data.put(Headers.DD , record.get(Headers.DD));
                data.put(Headers.FH , record.get(Headers.FH));
                data.put(Headers.T , record.get(Headers.T));
                data.put(Headers.SQ , record.get(Headers.SQ));
                data.put(Headers.P , record.get(Headers.P));
                data.put(Headers.VV , record.get(Headers.VV));
                data.put(Headers.U , record.get(Headers.U));
                Thread.sleep(timeInterval);

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

    public HashMap<Headers, String> getData() {
        return data;
    }

    @Value("${timer}")
    public void setTimeInterval(long timeInterval) {
        this.timeInterval = timeInterval;
    }

    @Value("${datafile}")
    public void setFile(String file) {
        this.file = file;
    }

    public long getTimeInterval() {
        return timeInterval;
    }

    public String getFile() {
        return file;
    }

}
