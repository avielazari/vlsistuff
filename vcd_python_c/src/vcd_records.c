
#include <stdlib.h>
#include "stdio.h"
#include "strings.h"
#include "ctype.h"
#include "string.h"

// #include "qq64.h"


FILE *Frecords;
FILE *Fregs;

void do_help() { return; }
void readfile(char *fname);

int debug = 0;
int linenum = 0;
int dones = 0;
int qdones = 0;
double start_time =0.0;
double end_time =0.0;
char fname1[500];
char fname2[500];
int main(argc, argv)
    int             argc;
    char           *argv[];

{
    char option[100];
    fname1[0] = 0;
    fname2[0] = 0;
    if (argc <= 1) do_help();
    if (argc > 1) {
        for (int k = 2; k <= argc; k++) {
            strcpy(option, *++argv);
            if (strcmp(option,"-debug")==0) {
                debug=1;
            } else if (strcmp(option,"-help")==0) {
              do_help();
            } else if (strcmp(option,"-start")==0) {
                    strcpy(option, *++argv);
                  start_time=atof(option);
                  k++;
            } else if (strcmp(option,"-end")==0) {
                    strcpy(option, *++argv);
                  end_time=atoi(option);
                  k++;
            } else if (fname1[0]==0) strcpy(fname1,option);
        }
    }
    if (fname2[0]==0) strcpy(fname2,"verilog.py");

    readfile(fname1);
}

int pscope = 0;
int scopes[1000];
char FULL[2000];

void wrapItUp() {
    fclose(Frecords);
    printf("%d lines read, %d records written %d regs written\n",linenum,dones,qdones);
    exit(0);
}


#define longestVal  200000
void readfile(fname) char *fname; {

    char s1[longestVal];
    char s2[longestVal];
    char s3[10000];
    char s4[10000];
    char s5[10000];
    char s6[10000];
    char s7[10000];

    FULL[0]=0;

    FILE *inf;
    inf = fopen(fname, "r");
    Frecords = fopen("recorded.nets","w");
    Fregs = fopen("recorded.regs","w");

   if (inf==NULL) {
        printf("error: cannot open input file %s\n",fname);
        exit(2);
    }
    int i,x;
    char *j;
    char line[longestVal];
    int searchEnd = 0;
    scopes[0]=0;
    j = (char *) 1;
    while ((j != NULL)&&(inf!=NULL)) {
        j = fgets(line, longestVal, inf);

        if (j==NULL) {
            exit(0);
        }

        i=sscanf(line,"%s %s %s %s %s %s %s",s1,s2,s3,s4,s5,s6,s7);
        linenum ++;

        if (i>0) {
            if (strcmp(s1,"$scope")==0) {
                if (strlen(FULL)>0) strcat(FULL,".");
                strcat(FULL,s3);

                pscope ++;
                scopes[pscope] = strlen(FULL);

            } else if (strcmp(s1,"$var")==0) {
                fprintf(Frecords,"record %8s %8s   %s.%s \n",s2,s4,FULL,s5);
                if (strcmp(s5,"Q")==0)  {
                    fprintf(Fregs,"reg %8s %8s   %s.%s \n",s2,s4,FULL,s5);
                    qdones ++;
                }
                dones ++;
            } else if (strcmp(s1,"$end")==0) {
                searchEnd = 1;
            } else if (strcmp(s1,"$upscope")==0) {
                pscope --;
                FULL[scopes[pscope]]=0;
            } else if (strcmp(s1,"$enddefinitions")==0) {
                wrapItUp();
            } else if (strcmp(s1,"$version")==0) {
                searchEnd = 1;
            } else if (strcmp(s1,"$date")==0) {
                searchEnd = 1;
            } else if (strcmp(s1,"$timescale")==0) {
                searchEnd = 1;
            } else if (strcmp(s1,"$comment")==0) {
                searchEnd = 1;

            } else if (searchEnd) {
                x = 0;
            } else {
                printf("bad line %s\n",line);
            }
        }
    }
}










