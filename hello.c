#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Anime
{
  char *title;
  double rating;
  char *info[50];
  int info_size;    //tracks the number of items added to info
};

// reads csv contents and returns array of anime
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
      }

      // Everything after title and rating are for comparison and will be added to info
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

double compare(struct Anime* a, struct Anime* b)
{
    printf("Title: %s\n",a[0].title);
    printf("Rating: %f\n",a[0].rating);
    for(int i = 0; i < a[0].info_size; i++)
    {
        printf("%s, ",a[0].info[i]);
    }

}

int main(int argc, char **argv)
{
  struct Anime* training = read_csv("test.csv");
  struct Anime* testing = read_csv("training.csv");

  // parallel for loop using 8 threads
    // for (int i = 0; i < 10; i++)
    // {
    //   for (int j = 0; j < 40; j++){

    //     // placeholder, comparison would  go here
    //     int r = rand() % 20;
    //     printf("Comparing %s vs %s. Result: %d\n",
    //                          testing[i].title, training[j].title, r);
    //   }
    // }

    compare(training, testing);

  free(training);
  free(testing);
  return 0;
}
