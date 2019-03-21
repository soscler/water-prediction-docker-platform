/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements. See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License. You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import java.io.IOException;

public class KafkaConsumerProducerDemo {
    public static void main(String[] args) {
        System.out.println("About to start kafka demo");
        boolean isAsync = args.length == 0 || !args[0].trim().equalsIgnoreCase("sync");

        FileDownloader fd = new FileDownloader(KafkaProperties.URL, KafkaProperties.CSV_FILE_NAME);
        try{
            fd.download();
            DataGenerator dataGenerator = new DataGenerator(KafkaProperties.CSV_FILE_NAME, KafkaProperties.CSV_READER_TIMER);

            Producer producerThread = new Producer(KafkaProperties.TOPIC, isAsync, dataGenerator);
            producerThread.start();

            Consumer consumerThread = new Consumer(KafkaProperties.TOPIC);
            consumerThread.start();
        } catch (IOException e){
            e.printStackTrace();
        }

    }
}
