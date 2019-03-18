package com.scac.server.stream.utils;


import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVRecord;

import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;
import java.util.Map;


public class CsvReader {

    final long timeInterval;

    public static enum Headers{
        ID,STN,YYYYMMDD,HH,DD,FH,FF,FX,T,T10,TD,SQ,Q,DR,RH,P,VV,N,U,WW,IX,M,R,S,O,Y
    }
    private Reader reader;
    private String file;
    private Map<Headers, String> data;


    public CsvReader(String file, long timer){
        this.file = file;
        this.timeInterval = timer;
    }


    public void read() throws IOException {
        System.out.println("About to read the csv file");
        reader = new FileReader(this.file);

        // TODO: Read a file from an url

        Iterable<CSVRecord> records = CSVFormat.RFC4180.withFirstRecordAsHeader().parse(this.reader);

        for (CSVRecord record : records) {
            try {

                /*String id = record.get(Headers.ID);
                String FH = record.get(Headers.FH);
                String YYYYMMDD = record.get(Headers.YYYYMMDD);
                String HH = record.get(Headers.HH);
                String DD = record.get(Headers.DD);
                String T = record.get(Headers.T);
                String SQ = record.get(Headers.SQ);
                String P = record.get(Headers.P);
                String VV = record.get(Headers.VV);
                String U = record.get(Headers.U);

                System.out.println("id: " + id);
                System.out.println("YYYYMMDD: " + YYYYMMDD);
                System.out.println("HH: " + HH);
                System.out.println("DD: " + DD);
                System.out.println("FH: " + FH);
                System.out.println("T: " + T);
                System.out.println("SQ: " + SQ);
                System.out.println("P: " + P);
                System.out.println("VV: " + VV);
                System.out.println("U: " + U);*/

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

                System.out.println(data.values());


                Thread.sleep(timeInterval);
            } catch (InterruptedException e)
            {
                e.printStackTrace();
            }

        }
    }

    public void push(){

    }

}
