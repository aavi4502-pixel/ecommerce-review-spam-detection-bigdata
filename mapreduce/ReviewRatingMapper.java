import java.io.IOException;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class ReviewRatingMapper
        extends Mapper<LongWritable, Text, Text, LongWritable> {

    private static final LongWritable ONE = new LongWritable(1);
    private final Text rating = new Text();

    @Override
    public void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {

        String line = value.toString();

        try {
            int start = line.indexOf("\"overall\"");

            if (start == -1) {
                return;
            }

            int colon = line.indexOf(":", start);

            if (colon == -1) {
                return;
            }

            int comma = line.indexOf(",", colon);

            if (comma == -1) {
                comma = line.indexOf("}", colon);
            }

            if (comma == -1) {
                return;
            }

            String ratingValue =
                    line.substring(colon + 1, comma)
                         .trim()
                         .replace("\"", "");

            rating.set(ratingValue);

            context.write(rating, ONE);

        } catch (Exception e) {
            // Ignore malformed records
        }
    }
}