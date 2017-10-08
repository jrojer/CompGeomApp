#include <cstdio>
#include <vector>

std::vector<std::pair<int,int>> ReadInput()
{
    std::vector<std::pair<int,int>> return_vector;
    char x;
    if(scanf("%c",&x) != 1 || x != 'P')
    {   
        printf("unrecognized input\n");
        return {};
    }
    unsigned num_points = 0;
    if (scanf("%u",&num_points) != 1)
    {   
        printf("unrecognized input\n");
        return  {};
    }
    for (unsigned i = 0; i< num_points;++i)
    {
        int x;
        int y;
        if (scanf("%d %d", &x,&y) != 2)
        {   
            printf("unrecognized input\n");
            return {};
        }
        return_vector.push_back({x,y});
    }
    return return_vector;
}

int main()
{
    auto &&points = ReadInput();

    if (!points.empty())
        printf("Good!\n");

    return 0;
}
