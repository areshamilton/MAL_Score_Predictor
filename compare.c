#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Anime
{
  char* title;
  int rank;
  double rating;
  char* info[3];
  double prediction;
  int avg_count;
};


// this function reads csv contents and returns array of anime
struct Anime* read_csv(char filename[])
{
  char buff[1024];
  int row_number = 0;
  int field_number = 0;
  int i = 0;
  struct Anime* dataset = malloc(sizeof(struct Anime) * 1000);
  FILE* in_file;
  in_file = fopen(filename, "r");

  if (in_file == NULL)
  {
    printf("file read failed\n");
    return dataset;
  }
  printf("%s\n\n", filename);
  while (fgets(buff, 1000, in_file))
  {
    field_number = 0;
    row_number++;
    // skipping the header
    if (row_number == 1) continue;
    char *field = strtok(buff, ",");

    while (field)
    {
      dataset[i].prediction = 0;
      dataset[i].avg_count = 0;
      if (field_number == 0) dataset[i].rank = atoi(field);
      if (field_number == 1)
      {
        (dataset + i)->title = malloc(strlen(field) + 1);
        strcpy((dataset + i)->title, field);
      }
      if (field_number == 2) dataset[i].rating = strtod(field, NULL);
      if (field_number == 3)
      {
        (dataset + i)->info[0] = malloc(strlen(field) + 1);
        strcpy((dataset + i)->info[0], field);
      }
      if (field_number == 4)
      {
        (dataset + i)->info[1] = malloc(strlen(field) + 1);
        strcpy((dataset + i)->info[1], field);
      }
      if (field_number == 5)
      {
        (dataset + i)->info[2] = malloc(strlen(field) + 1);
        strcpy((dataset + i)->info[2], field);
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
  fprintf(out_file, "Title, Prediction\n");
  for (unsigned i = 0; i < 10; i++)
  {
    fprintf(out_file, "%s, %f\n", dataset[i].title, dataset[i].prediction);
  }
  fclose(out_file);
}


// this function compares string similarity using levenshtein distance
int distance(char* a, char* b)
{
  unsigned a_size = strlen(a);
  unsigned b_size = strlen(b);
  unsigned int comp_matrix[a_size+1][b_size+1];
  comp_matrix[0][0] = 0;

  for (unsigned i = 0; i <= a_size; i++)
  {
    comp_matrix[i][0] = i;
  }
  for (unsigned i = 0; i <= b_size; i++)
  {
    comp_matrix[0][i] = i;
  }
  for (unsigned i = 1; i <= a_size; i++)
  {
    char x = a[i-1];
    for (unsigned j = 1; j <= b_size; j++)
    {
      char y = b[j-1];
      if (x == y)
      {
        comp_matrix[i][j] = comp_matrix[i-1][j-1];
      } else
      {
        int min, del, ins, sub;
        del = comp_matrix[i-1][j] + 1;
        ins = comp_matrix[i][j-1] + 1;
        sub = comp_matrix[i-1][j-1] + 1;
        min = del;
        if (ins < min) min = ins;
        if (sub < min) min = sub;
        comp_matrix[i][j] = min;
      }
    }
  }
  return comp_matrix[a_size][b_size];
}


// this function returns the greater of two values
int greater(char* a, char* b)
{
  if (strlen(a) >= strlen(b)) return strlen(a);
  else return strlen(b);
}


int main(int argc, char **argv)
{
  omp_set_num_threads(8);

  struct Anime* training = read_csv("training.csv");
  struct Anime* testing = read_csv("test.csv");

  // parallel for loop used to compare anime
  #pragma omp parallel for collapse(2)
    for (unsigned i = 0; i < 10; i++)
    {
      for (unsigned j = 0; j < 40; j++){
        char* anime_1 = testing[i].title;
        char* anime_2 = training[j].title;
        double dis = (double)distance(testing[i].info[1], training[j].info[1]);
        double length = (double)greater(testing[i].info[1], training[j].info[1]);
        double similarity = (length - dis) / length;
        if (similarity >= 0.8)
        {
          testing[i].prediction += training[j].rating;
          testing[i].avg_count++;
        }
        printf("Thread %d - Similarity between %s and %s is %f\n",
                omp_get_thread_num(), anime_1, anime_2, similarity);
      }
    }

  // parallel for loop used to show the average rating of each anime
  // based on ratings of similar anime
  #pragma omp parallel for
    for (unsigned i = 0; i < 10; i++)
    {
      testing[i].prediction = testing[i].prediction / testing[i].avg_count;
      printf("Thread %d: Average rating of %s: %f\n",
              omp_get_thread_num(), testing[i].title, testing[i].prediction);
    }
    printf("%s", testing[4].title);
  write_csv(testing);
  free(training);
  free(testing);
  return 0;
}
