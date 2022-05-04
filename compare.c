#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Anime
{
  char *title;
  int rank;
  double rating;
  char *info[3];
};

// reads csv contents and returns array of anime
struct Anime *read_csv(char filename[])
{
  char buff[1024];
  int row_number = 0;
  int field_number = 0;
  int i = 0;
  struct Anime *dataset = malloc(sizeof(struct Anime) * 1000);
  FILE *in_file;
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

int main(int argc, char **argv)
{
  omp_set_num_threads(8);

  struct Anime* training = read_csv("training.csv");
  struct Anime* testing = read_csv("test.csv");

  // parallel for loop using 8 threads
  #pragma omp parallel for collapse(2)
    for (int i = 0; i < 10; i++)
    {
      for (int j = 0; j < 40; j++){

        // placeholder, comparison would  go here
        int r = rand() % 20;
        printf("Thread %d comparing '%s' vs '%s'. Result: %d\n",
                omp_get_thread_num(), testing[i].title, training[j].title, r);
      }
    }


  free(training);
  free(testing);
  return 0;
}
