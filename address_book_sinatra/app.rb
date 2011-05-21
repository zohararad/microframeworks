require 'sinatra'
require 'haml'
require 'mongoid'

require './models/address'

## Configuration area ##

configure do
   Mongoid.configure do |config|
    name = "address_book"
    host = "localhost"
    config.master = Mongo::Connection.new.db(name)
    config.slaves = [
      Mongo::Connection.new(host, 27017, :slave_ok => true).db(name)
    ]
    config.persist_in_safe_mode = false
  end
end

helpers do
  def partial(page, options={})
    haml page, options.merge!(:layout => false)
  end
end

## end Configuration area ##

get '/' do
  @addresses = Address.all
  haml :index
end

get '/address/new' do
  @form_url = url('/address')
  @address = Address.new
  haml :new
end

post '/address' do
  address = Address.new(params[:address])
  address.save
  redirect to("/address/#{address.id}")
end

get '/address/:id' do
  @address = Address.find(params[:id])
  haml :show
end

get '/address/:id/edit' do
  @form_url = url('/address/%s' % params[:id])
  @address = Address.find(params[:id])
  haml :edit
end

post '/address/:id' do
  @address = Address.find(params[:id])
  @address.update_attributes(params[:address])
  redirect to("/address/#{@address.id}")
end

get '/address/:id/delete' do
  address = Address.find(params[:id])
  address.destroy
  redirect to('/')
end