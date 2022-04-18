import graphene
from graphene_django import DjangoObjectType
from .models import Director, Movie
import graphql_jwt
from graphql_jwt.decorators import login_required

# object type for model director
class DirectorType(DjangoObjectType):
    class Meta:
        model = Director

    # extra field and function for fetch.
    fullname = graphene.String()

    def resolve_fullname(self, info, **kwargs):
        return self.first_name + " " + self.last_name


# object type for model Movie
class MovieType(DjangoObjectType):
    class Meta:
        model = Movie


# all queries are written here.
class Query(graphene.ObjectType):
    all_movies = graphene.List(MovieType)
    all_directors = graphene.List(DirectorType)
    movie_detail = graphene.Field(
        MovieType, id=graphene.Int(), title=graphene.String()
    )
    director_detail = graphene.Field(DirectorType, id=graphene.Int())

    # for fetch all movies in db
    @login_required
    def resolve_all_movies(self, info, **kwargs):
        return Movie.objects.all()

    # for fetch all directors in db
    def resolve_all_directors(self, info, **kwargs):
        return Director.objects.all()

    # to fetch a single movie by id and title
    def resolve_movie_detail(self, info, **kwargs):
        id = kwargs.get("id")
        title = kwargs.get("title")

        if id is not None:
            return Movie.objects.get(pk=id)
        if title is not None:
            return Movie.objects.get(title=title)
        else:
            return None

    # to fetch a single director by id
    def resolve_director_detail(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return Director.objects.get(pk=id)
        else:
            return None


# mutations are used to modify server-side data like create,update and delete.
class DirectorCreateMutation(graphene.Mutation):
    # ‘class argument’ allows us to define a parameter to save data to the database.specifies the fields.
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)

    director = graphene.Field(DirectorType)

    def mutate(self, info, first_name, last_name):
        director = Director.objects.create(
            first_name=first_name, last_name=last_name
        )
        return DirectorCreateMutation(director=director)


class DirectorUpdateMutation(graphene.Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        id = graphene.ID(required=True)

    director = graphene.Field(DirectorType)

    def mutate(self, info, id, first_name, last_name):
        director = Director.objects.get(pk=id)
        if first_name is not None:
            director.first_name = first_name
        if last_name is not None:
            director.last_name = last_name
        director.save()

        return DirectorUpdateMutation(director=director)


class DirectorDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    director = graphene.Field(DirectorType)

    def mutate(self, info, id):
        director = Director.objects.get(pk=id)
        director.delete()

        return DirectorDeleteMutation(director=None)


# ‘class Mutation’ defines our mutations and sends parameters such as updating and creating data to the model.
class Mutation:

    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    create_director = DirectorCreateMutation.Field()
    update_director = DirectorUpdateMutation.Field()
    delete_director = DirectorDeleteMutation.Field()
