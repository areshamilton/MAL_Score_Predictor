#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

struct Anime
{
  char* title;
  double rating;
  char* info[50];
  int info_size;
  double prediction;
  double avg_count;
};


// this function reads csv contents and returns array of anime
struct Anime *read_csv(char filename[])
{
  char buff[1024];
  int row_number = 0;
  int field_number = 0;
  int i = 0;
  struct Anime *dataset = malloc(sizeof(struct Anime) * 2000);
  FILE *in_file;
  in_file = fopen(filename, "r");

  if (in_file == NULL)
  {
    printf("file read failed\n");
    return dataset;
  }

  printf("Reading: %s\n\n", filename);
  while (fgets(buff, 1000, in_file))
  {
    field_number = 0;
    row_number++;
    // skipping the header
    //if (row_number == 1) continue;
    char *field = strtok(buff, ",");

    while (field)
    {
      if(field_number == 0)
      {
          //printf("%s ",field);
          (dataset + i)->title = malloc(strlen(field) + 1);
          strcpy((dataset + i)->title, field);

      }
      if(field_number == 1)
      {
          char *temp = field + 2;
          temp[strlen(temp)-1] = '\0';
          dataset[i].rating = strtod(temp, NULL);
          dataset[i].prediction = 1.0;
          dataset[i].avg_count = 1.0;
      }

      // Everything after title and rating are for comparison and will be added to info[]
      if(field_number > 1)
      {
        int index = field_number - 2;
        (dataset + i)->info[index] = malloc(strlen(field) + 1);
        strcpy((dataset + i)->info[index], field);
        dataset[i].info_size = index + 1;
      }
      field = strtok(NULL, ",");
      field_number++;
    }
    i++;
  }
  fclose(in_file);
  return dataset;
}


// this function writes a title and its predicted rating onto a csv file
void write_csv(struct Anime* dataset)
{
  FILE* out_file;
  out_file = fopen("predictions.csv", "w+");
  //fprintf(out_file, "Title, Prediction\n");
  for (unsigned i = 0; i < 412; i++)
  {
    fprintf(out_file, "%s, %f\n", dataset[i].title, dataset[i].prediction);
  }
  fclose(out_file);
}

double compare(struct Anime a, struct Anime b)
{
    double match_count = 0.0;
    double similarity;
    for(int i = 0; i < a.info_size; i++)
    {
        for (int j = 0; j < b.info_size; j++)
        {
          if (strcmp(a.info[i], b.info[j]) == 0) match_count++;
        }
    }
    similarity = match_count / ((a.info_size + b.info_size) - match_count);
    return similarity;
}

int main(int argc, char **argv)
{
  omp_set_num_threads(8);

  clock_t begin = clock();

  struct Anime* training = read_csv("training.csv");
  struct Anime* testing = read_csv("test.csv");

  int tid;
  double local_avg;
  double local_predict;
  double similarity_threshold = -1.0;
  double elapsed = 0.0;
  double similarity_avg = 0.0;

    #pragma omp parallel for 
    for (int i = 0; i < 412; i++)
      {
        local_avg = 0.0;
        local_predict = 0.0;
        tid = omp_get_thread_num();
        #pragma omp parallel for reduction(+:local_avg,local_predict,similarity_avg)
        for (int j = 0; j < 1859; j++)
        {
          double similarity = compare(testing[i], training[j]);
          similarity_avg += similarity;
          //tid = omp_get_thread_num();
          printf("Thread [%d] Comparing %s vs %s Similarity: %f\n", 
                    tid, testing[i].title, training[j].title, similarity);
          if(similarity >= similarity_threshold && training[j].rating > 0)
          {
            local_avg++;
            local_predict += training[j].rating;
          }
        }
        testing[i].avg_count = local_avg;
        testing[i].prediction = local_predict;
      }
    

  // parallel for loop used to show the average rating of each anime
  // based on ratings of similar anime
  int not_predicted = 0.0;
  #pragma omp parallel for reduction(+:not_predicted)
    for (unsigned i = 0; i < 412; i++)
    {
      if(testing[i].avg_count > 0)
      {
          testing[i].prediction = testing[i].prediction / testing[i].avg_count;
      }
      else
      {
          testing[i].prediction = -1;
          not_predicted++;
      }
      printf("Thread %d: Average rating of %s: %f\n",
              omp_get_thread_num(), testing[i].title, testing[i].prediction);
    }
    clock_t end = clock();
    elapsed = (double)(end - begin) / CLOCKS_PER_SEC;
    printf("Number of failed predictions: %d\n",not_predicted);
    printf("Elapsed time in seconds: %f\n", elapsed);
  write_csv(testing);
  free(training);
  free(testing);
  return 0;
}